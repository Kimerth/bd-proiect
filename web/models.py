from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    uid = models.IntegerField(default=0, unique=True)

    class Meta:
        permissions = [
            ("see_basic", "See Departments and Buildings"),
            ("see_experiments", "See Experiments"),
            ("see_results", "See Results"),
            ("see_tools", "See Tools"),
            ("see_researchers", "See Researchers"),
            ("add_basic", "Add new Departments and Buildings"),
            ("add_experiments", "Add new Experiments"),
            ("add_results", "Add new Results"),
            ("add_tools", "Add new Tools"),
            ("add_researchers", "Add new Researchers"),
            ("remove_basic", "Remove Departments and Buildings"),
            ("remove_experiments", "Remove Experiments"),
            ("remove_results", "Remove Results"),
            ("remove_tools", "Remove Tools"),
            ("remove_researchers", "Remove Researchers"),
            ("modify_basic", "Modify Departments and Buildings"),
            ("modify_experiments", "Modify Experiments"),
            ("modify_results", "Modify Results"),
            ("modify_tools", "Modify Tools"),
            ("modify_researchers", "Modify Researchers"),
        ]