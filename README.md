# Password Strength Checker

A beginner Python tool that analyzes a password and tells you how strong it is.

## What it checks
- Length (at least 8 characters, and at least 12 before a mixed password is called strong)
- Uppercase and lowercase letters, including letters outside the English alphabet
- Numbers
- Any character that is not a letter or number, such as `!`, `-`, or a space
- Common passwords, repeated characters (`aaaa`), and straight sequences (`abcd`, `123`)
- Long passphrases of three or more words (16 characters or more)

## How to run

```
python password_checker.py
```

Typing a password in the terminal hides it. The checks are in `check_password_strength`, so they can be tested without typing:

```
python -m unittest
```

## Example output

```
Enter a password to check: hello
Password Strength: Weak (1/5)
Tips to improve:
  - This matches a very common password. Use words that are not famous or easy to guess.
  - Use at least 8 characters
  - Add at least one uppercase letter
  - Add at least one number
  - Add a special character, space, or hyphen
```

`Password1!` used to be reported as Strong (5/5). It is now Weak, because it is a common pattern with a capital letter, a number, and a symbol added on.
