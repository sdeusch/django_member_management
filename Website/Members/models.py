from django.db import models


class Member(models.Model):
    '''A Member is a unique User that can belong to different Accounts (Insurers) '''
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone_number=models.IntegerField()
    client_member_id=models.IntegerField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Account(models.Model):
    ''' An instance of this class represents a mapping of a Member to an Account
        Uniqueness is guaranteed by a uniqueness constraint in the Meta class

        @Todo: If we want to more attributes create new Model class
     '''
    member=models.ForeignKey(Member, on_delete=models.CASCADE)
    account_id = models.IntegerField()

    class Meta:
        constraints = [
                    models.UniqueConstraint(name='account_member_uq', fields=['account_id', 'member'])
        ]

    def __str__(self):
        return self.member.first_name + ' ' + self.member.last_name + ', Account ' + str(self.account_id)


class MemberCSVFileUpload(models.Model):
    '''Our CSV file upload class'''
    fname = models.CharField(max_length=500)
    file = models.FileField(upload_to='uploads/csv/')

    def __str__(self):
        self.fname
