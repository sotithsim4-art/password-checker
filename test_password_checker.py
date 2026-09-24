import unittest

import password_checker


class PasswordCheckerTests(unittest.TestCase):
    def test_short_common_word_stays_weak(self):
        strength, score, feedback = password_checker.check_password_strength("hello")
        self.assertEqual(strength, "Weak")
        self.assertLessEqual(score, 2)
        self.assertTrue(any("common" in tip.lower() for tip in feedback))

    def test_familiar_mix_is_not_strong(self):
        for password in ("Password1!", "Qwerty123!", "P@ssw0rd", "Summer2024!", "Tr0ub4dor&3"):
            strength, score, _ = password_checker.check_password_strength(password)
            self.assertEqual(strength, "Weak", password)
            self.assertLessEqual(score, 2, password)

    def test_repeats_and_sequences_are_not_strong(self):
        for password in ("Aa1!aaaa", "aaaaAAAA1!", "abcABC123!"):
            strength, _, feedback = password_checker.check_password_strength(password)
            self.assertEqual(strength, "Weak", password)
            self.assertTrue(feedback, password)

    def test_hyphen_counts_and_long_unique_password_can_be_strong(self):
        strength, score, _ = password_checker.check_password_strength("Correct-Horse-1")
        self.assertEqual((strength, score), ("Strong", 5))

    def test_long_passphrase_does_not_need_symbols(self):
        strength, score, feedback = password_checker.check_password_strength("correct-horse-battery")
        self.assertEqual((strength, score), ("Strong", 5))
        self.assertEqual(feedback, [])

    def test_unicode_letters_count(self):
        cyrillic, _, cyrillic_tips = password_checker.check_password_strength("парольПароль1!")
        self.assertEqual(cyrillic, "Strong")
        self.assertFalse(any("uppercase" in tip.lower() for tip in cyrillic_tips))

        nordic, score, tips = password_checker.check_password_strength("ÅäöÅäö12!")
        self.assertEqual(nordic, "Medium")
        self.assertEqual(score, 4)
        self.assertTrue(any("12 characters" in tip for tip in tips))

    def test_blank_input_does_not_earn_length(self):
        for password in ("", " ", "        ", None):
            strength, score, feedback = password_checker.check_password_strength(password)
            self.assertEqual((strength, score), ("Weak", 0), repr(password))
            self.assertTrue(feedback)


if __name__ == "__main__":
    unittest.main()
