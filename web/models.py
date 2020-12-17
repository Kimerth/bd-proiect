from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        permissions = [
            ("see_basic", "See Departments and Buildings"),
            ("see_experiments", "See Experiments"),
            ("see_results", "See Results"),
            ("see_tools", "See Tools"),
            ("see_researchers", "See Researchers"),
            ("add_basic", "Add new Departments and Buildings"),
            ("add_experiments", "Add mew Experiments"),
            ("add_results", "Add new Results"),
            ("add_tools", "Add new Tools"),
            ("add_researchers", "Add new Researchers"),
        ]