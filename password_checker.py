import getpass
import re
import sys

COMMON_PASSWORDS = {
    "password", "password1", "password123", "qwerty", "qwerty123",
    "letmein", "admin", "admin123", "welcome", "iloveyou", "sunshine",
    "princess", "football", "monkey", "dragon", "master", "login",
    "abc123", "trustno1", "changeme", "secret", "hello", "summer",
    "winter", "spring", "autumn", "passw0rd", "p@ssw0rd", "123456",
    "12345678", "123456789", "1234567890", "111111", "000000",
    "tr0ub4dor&3",
}

LEET = str.maketrans({
    "@": "a",
    "0": "o",
    "1": "i",
    "3": "e",
    "4": "a",
    "5": "s",
    "7": "t",
    "$": "s",
})


def is_common_password(password):
    lowered = password.lower()
    folded = lowered.translate(LEET)
    candidates = {lowered, folded}
    for value in (lowered, folded):
        letters = "".join(ch for ch in value if ch.isalpha())
        if letters:
            candidates.add(letters)
    if any(candidate in COMMON_PASSWORDS for candidate in candidates):
        return True
    parts = [part for part in re.split(r"[\s\-]+", password) if part]
    return any(part != password and is_common_password(part) for part in parts)


def has_repeated_run(password, length=4):
    lowered = password.lower()
    for start in range(len(lowered) - length + 1):
        if len(set(lowered[start:start + length])) == 1:
            return True
    return False


def has_straight_sequence(text, length):
    for start in range(len(text) - length + 1):
        chunk = text[start:start + length]
        steps = [ord(chunk[i + 1]) - ord(chunk[i]) for i in range(length - 1)]
        if all(step == 1 for step in steps) or all(step == -1 for step in steps):
            return True
    return False


def has_predictable_sequence(password):
    lowered = password.lower()
    letters = "".join(ch for ch in lowered if ch.isalpha())
    digits = "".join(ch for ch in lowered if ch.isdigit())
    return has_straight_sequence(letters, 4) or has_straight_sequence(digits, 3)


def is_long_passphrase(password):
    words = [
        word for word in re.split(r"[\s\-]+", password)
        if sum(ch.isalpha() for ch in word) >= 3
    ]
    return len(password) >= 16 and len(words) >= 3


def check_password_strength(password):
    if not isinstance(password, str) or password.strip() == "":
        return "Weak", 0, ["Enter a password. Spaces alone do not count."]

    feedback = []
    score = 0

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    if any(ch.isupper() for ch in password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter")

    if any(ch.islower() for ch in password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter")

    if any(ch.isdigit() for ch in password):
        score += 1
    else:
        feedback.append("Add at least one number")

    if any(not ch.isalnum() for ch in password):
        score += 1
    else:
        feedback.append("Add a special character, space, or hyphen")

    pattern_notes = []
    if is_common_password(password):
        pattern_notes.append(
            "This matches a very common password. Use words that are not famous or easy to guess."
        )
    if has_repeated_run(password):
        pattern_notes.append("Avoid repeating the same character four times in a row.")
    if has_predictable_sequence(password):
        pattern_notes.append("Avoid straight sequences such as abcd or 123.")

    if pattern_notes:
        return "Weak", min(score, 2), pattern_notes + feedback

    if is_long_passphrase(password):
        return "Strong", 5, []

    if score == 5 and len(password) >= 12:
        return "Strong", score, feedback

    if score == 5:
        score = 4
        feedback.append("Use at least 12 characters before treating a password as strong.")

    if score >= 3 or len(password) >= 12:
        return "Medium", score, feedback

    return "Weak", score, feedback


def report(password):
    strength, score, feedback = check_password_strength(password)
    print(f"\nPassword Strength: {strength} ({score}/5)")
    if feedback:
        print("Tips to improve:")
        for tip in feedback:
            print(f"  - {tip}")
    return strength, score, feedback


def read_password():
    prompt = "Enter a password to check: "
    if sys.stdin.isatty():
        return getpass.getpass(prompt)
    password = sys.stdin.readline()
    if password.endswith("\r\n"):
        return password[:-2]
    if password.endswith("\n"):
        return password[:-1]
    return password


if __name__ == "__main__":
    report(read_password())
