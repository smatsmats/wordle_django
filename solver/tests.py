from django.test import SimpleTestCase

from . import engine


class SolverTests(SimpleTestCase):
    def test_known_letter_and_exclude(self):
        r = engine.solve(known=["c", "", "", "", ""], exclude="i")
        self.assertTrue(r["words"])
        self.assertTrue(all(w[0] == "c" and "i" not in w for w in r["words"]))

    def test_include_no_repeats(self):
        r = engine.solve(include="ra", no_repeats=True)
        self.assertTrue(all("r" in w and "a" in w and len(set(w)) == 5 for w in r["words"]))

    def test_api_and_bad_regex(self):
        self.assertEqual(self.client.get("/api/solve?p1=c").status_code, 200)
        self.assertEqual(self.client.get("/api/solve?regex=(").status_code, 400)
        self.assertEqual(self.client.get("/healthz").status_code, 200)
        self.assertContains(self.client.get("/?p1=c&include=r"), "candidate word")
