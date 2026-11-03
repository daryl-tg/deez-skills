import subprocess

EXIT_WAIT_S = 10
POLL_S = 0.5
TAKEOVER_WARNING = (
    "Take over {ticket}? A live Worker is killed first, and a later input can revive it."
)


def run_tmux(argv):
    return subprocess.run(argv)


class TakeoverMixin:
    def init_takeover(self, tmux, in_tmux, pid_alive, sleep):
        self.tmux = tmux
        self.in_tmux = in_tmux
        self.pid_alive = pid_alive
        self.sleep = sleep
        self.taken_over = set()

    def action_takeover(self):
        row = self.current_ticket()
        missing = "session" if not row.session_id else "worktree" if not row.worktree else None
        if missing:
            self.notify(f"{row.ticket_id}: no {missing} to resume", severity="warning", markup=False)
            return
        self.ask(
            TAKEOVER_WARNING.format(ticket=row.ticket_id),
            lambda: self.run_worker(lambda: self.takeover(row), thread=True, exit_on_error=False),
        )

    def takeover(self, row):
        if self.pid_alive(row.pid):
            result = self.verb(self.argv("kill", row.assignment_id))
            if result.returncode != 0:
                self.call_from_thread(self.verb_done, result.argv, result, None)
                return
            deadline = self.clock() + EXIT_WAIT_S
            while self.pid_alive(row.pid):
                if self.clock() >= deadline:
                    self.call_from_thread(
                        self.notify, f"{row.ticket_id}: Worker did not exit within {EXIT_WAIT_S}s",
                        severity="error", markup=False,
                    )
                    return
                self.sleep(POLL_S)
        self.call_from_thread(self.open_session, row)

    def open_session(self, row):
        argv = ["claude", "--resume", row.session_id]
        if self.in_tmux():
            self.tmux(["tmux", "new-window", "-n", row.slug, "-c", row.worktree, *argv])
        else:
            with self.suspend():
                subprocess.run(argv, cwd=row.worktree)
        self.taken_over.add(row.ticket_id)
        self.render_rows()
        self.refresh_snapshot()
