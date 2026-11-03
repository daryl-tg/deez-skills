import subprocess

EXIT_WAIT_S = 10
POLL_S = 0.5
TMUX_TIMEOUT_S = 5
TAKEOVER_WARNING = (
    "Take over {ticket}? A live Worker is killed first, and a later input can revive it."
)


def run_tmux(argv):
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=TMUX_TIMEOUT_S)
    except (OSError, subprocess.SubprocessError) as exc:
        return subprocess.CompletedProcess(argv, 127, "", str(exc))


class TakeoverMixin:
    def init_takeover(self, tmux, in_tmux, pid_alive, sleep):
        self.tmux = tmux
        self.in_tmux = in_tmux
        self.pid_alive = pid_alive
        self.sleep = sleep
        self.taken_over = set()
        self.title_wanted = "board"
        self.title_busy = False

    def takeover_refusal(self, row):
        if row.ticket_id in self.taken_over:
            return f"{row.ticket_id}: already taken over"
        if not row.session_id:
            return f"{row.ticket_id}: no session to resume"
        if not row.worktree:
            return f"{row.ticket_id}: no worktree to resume"
        return None

    def action_takeover(self):
        row = self.current_ticket()
        reason = self.takeover_refusal(row)
        if reason:
            self.notify(reason, severity="warning", markup=False)
            return
        self.ask(TAKEOVER_WARNING.format(ticket=row.ticket_id), lambda: self.begin_takeover(row.ticket_id))

    def begin_takeover(self, ticket_id):
        row = next((row for row in self.snap.rows if row.ticket_id == ticket_id), None)
        reason = f"{ticket_id}: no longer on the board" if row is None else self.takeover_refusal(row)
        if reason:
            self.notify(reason, severity="warning", markup=False)
            return
        self.run_worker(lambda: self.takeover(row), thread=True, exit_on_error=False)

    def takeover(self, row):
        try:
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
            if self.in_tmux():
                done = self.tmux(["tmux", "new-window", "-n", row.slug, "-c", row.worktree, *self.resume_argv(row)])
                error = None if done.returncode == 0 else f"tmux new-window exited {done.returncode}"
                self.call_from_thread(self.session_opened, row, error)
            else:
                self.call_from_thread(self.resume_in_foreground, row)
        except Exception as exc:
            self.call_from_thread(self.session_opened, row, f"takeover failed: {exc}")

    def resume_argv(self, row):
        return ["claude", "--resume", row.session_id]

    def resume_in_foreground(self, row):
        error = None
        try:
            with self.suspend():
                subprocess.run(self.resume_argv(row), cwd=row.worktree)
        except OSError as exc:
            error = f"claude could not start: {exc}"
        self.session_opened(row, error)

    def session_opened(self, row, error):
        if error:
            self.notify(f"{row.ticket_id}: {error}", severity="error", markup=False)
        else:
            self.taken_over.add(row.ticket_id)
            self.render_rows()
        self.refresh_snapshot()
