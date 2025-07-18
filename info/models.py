from django.db import models

class studentinfo(models.Model):
    rollno=models.IntegerField(primary_key=True)
    name=models.TextField(max_length=50)
    password=models.TextField(max_length=20)
    confpass=models.TextField(max_length=20)
    phoneno=models.BigIntegerField()
    email=models.EmailField()
    image=models.ImageField(upload_to='student_photos/')

class Marks(models.Model):
    student = models.OneToOneField(studentinfo, on_delete=models.CASCADE)
    english = models.IntegerField()
    hindi = models.IntegerField()
    telugu = models.IntegerField()
    maths = models.IntegerField()
    science = models.IntegerField()
    social = models.IntegerField()

    def has_failed(self):
        subjects = [
            self.english, self.hindi, self.telugu,
            self.maths, self.science, self.social
        ]
        return any(mark < 35 for mark in subjects)

    def result_status(self):
        return "FAIL" if self.has_failed() else "PASS"

    def __str__(self):
        return f"Marks for {self.student.name} (Roll: {self.student.rollno})"
