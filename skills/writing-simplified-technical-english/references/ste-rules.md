# ASD-STE100 rules for agent documents

Source: ASD-STE100 Simplified Technical English, Issue 9, 2025-01-15. Part 1
has 53 rules in 9 sections. Part 2 is a dictionary of approved words.

This file gives the rules that apply to agent instruction documents, with their
Issue 9 numbers. It does not reproduce the standard or its dictionary. ASD
gives the full document at no cost: https://www.asd-ste100.org/.

## Words (section 1)

- **1.1** Use approved words, technical nouns, and technical verbs only.
- **1.2, 1.3** Use each word with one part of speech and one meaning.
- **1.5, 1.6, 1.8, 1.12** A word that the dictionary does not approve is still
  permitted as a technical noun or a technical verb. It must belong to your
  subject field. Your repository vocabulary is such a set.
- **1.11** Do not use different names for the same item. One concept keeps one
  name in the document.
- **1.14** Use American English spelling.

## Multi-word nouns (section 2)

- **2.1** Use a maximum of three words in a multi-word noun. `feature worktree
  branch` is permitted. `primary worktree branch promotion step` is not.
- **2.2** When a technical noun needs more than three words, write it in full
  once. Then give a short form, or put hyphens between the words that operate
  as one unit.

## Verbs (section 3)

- **3.2** Use these forms only: the infinitive, the imperative, the simple
  present, the simple past, the simple future, and the past participle as an
  adjective.
- **3.4** Do not use auxiliary verbs to make complex constructions. Write "the
  gate failed", not "the gate has failed".
- **3.5** Use an `-ing` form only as a technical noun, or inside one.
- **3.6** Use the active voice. The passive voice is permitted in descriptive
  text only when the agent of the action is unknown.
- **3.7** Use a verb for an action, not a noun. Write "analyze the log", not
  "do an analysis of the log".

## Sentences (section 4)

- **4.2** Do not remove words, and do not use contractions, to make a sentence
  shorter. A missing article or verb adds ambiguity.
- **4.3** Use a vertical list for a complex text. A numbered list, a table, and
  a code fence all satisfy this rule.
- **4.5** Put an article (the, a, an) or a demonstrative adjective (this,
  these) before a noun when English permits one.

## Procedures (section 5)

- **5.1** Use a maximum of 20 words in a sentence. Most of an agent document is
  procedural, so this is the usual limit.
- **5.2** Write one instruction in each sentence, unless two actions occur at
  the same time.
- **5.3** Write an instruction in the imperative form.
- **5.4** When the reader must know a condition first, start with the
  condition. Then put a comma before the command.
- **5.5** A note gives information only. Never put an instruction in a note.

## Descriptive text (section 6)

- **6.3** Use a maximum of 25 words in a sentence.
- **6.5** Give each paragraph one topic.
- **6.6** Use a maximum of six sentences in a paragraph.

## Safety instructions (section 7)

Agent documents have the same category: the stop conditions and prohibitions
that prevent damage.

- **7.1** Name the level of risk with a constant word.
- **7.2** Put the safety instruction before the step it controls, and start it
  with the command or the condition.
- **7.3** Give the risk or the result after the command.

## Punctuation and word count (section 8)

- **8.1** All standard punctuation marks are permitted, but not the semicolon.
- **8.2** Use hyphens between words that are directly related.
- **8.3** Parentheses are permitted for references, identifiers, abbreviations,
  and alternatives.
- **8.4** In a vertical list, a colon ends a sentence for the word count.
- **8.5** Text inside parentheses counts as one word.
- **8.6** Each of these counts as one word: a number, a number with its unit,
  an abbreviation, an alphanumeric identifier, quoted text, a title, and a
  proper noun.
- **8.7** A hyphenated word counts as one word.

Rules 8.5 and 8.6 matter here. A path, a command, a branch pattern, and a
quoted string each count as one word against the 20-word limit.

## Writing practices (section 9)

- **9.1** When a word-for-word replacement is not sufficient, write the
  sentence again with a different construction.
- **9.3** Do not put two words together to make a phrasal verb. Write "start
  the run", not "kick off the run". Write "read the plan", not "dive into the
  plan".
- **9.4** Keep one style for terminology and wording through the document.

## Where agent documents differ

1. **Domain vocabulary stays.** `worktree`, `subagent`, `frontmatter`,
   `rebase`, and `commit` are technical nouns and technical verbs under Rules
   1.5, 1.6, and 1.12. Do not translate them.
2. **A skill name is a technical noun.** Rule 3.5 does not change
   `writing-plans` or any other identifier.
3. **Modality has priority over Rule 3.4.** When a compound verb carries
   uncertainty that the simple form loses, keep the compound form and report
   it. "The gate can fail" is not "the gate fails".
