from kivymd.uix.screen import MDScreen

class Feature4_Screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def calculate_gpa(self, participation_score, midterm_score, final_score):
        try:
            participation_score = float(participation_score) if participation_score else 0
            midterm_score = float(midterm_score) if midterm_score else 0
            final_score = float(final_score) if final_score else 0

            gpa_10 = (participation_score * 0.1) + (midterm_score * 0.4) + (final_score * 0.5)

            fractional_part = gpa_10 % 1
            if fractional_part < 0.45:
                rounded_gpa_10 = round(gpa_10 - fractional_part, 1)
            else:
                rounded_gpa_10 = round(gpa_10 - fractional_part + 0.5, 1)

            if rounded_gpa_10 >= 9.0:
                letter_grade, gpa_4 = "A+", 4.0
            elif rounded_gpa_10 >= 8.5:
                letter_grade, gpa_4 = "A", 4.0
            elif rounded_gpa_10 >= 8.0:
                letter_grade, gpa_4 = "B+", 3.5
            elif rounded_gpa_10 >= 7.0:
                letter_grade, gpa_4 = "B", 3.0
            elif rounded_gpa_10 >= 6.5:
                letter_grade, gpa_4 = "C+", 2.5
            elif rounded_gpa_10 >= 5.5:
                letter_grade, gpa_4 = "C", 2.0
            elif rounded_gpa_10 >= 5.0:
                letter_grade, gpa_4 = "D+", 1.5
            elif rounded_gpa_10 >= 4.0:
                letter_grade, gpa_4 = "D", 1.0
            else:
                letter_grade, gpa_4 = "F", 0.0

            self.ids.gpa_result.text = f"Projected GPA: {gpa_10:.2f}\nGrade: {letter_grade} (4.0 Scale: {gpa_4})"
        except ValueError:
            self.ids.gpa_result.text = "Please enter valid scores for participation, midterm, and final exam."