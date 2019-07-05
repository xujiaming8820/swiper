from django.db import models


# Create your models here.
class Swiped(models.Model):
    MARKS = (
        ('like', '喜欢'),
        ('dislike', '不喜欢'),
        ('superlike', '超级喜欢'),
    )

    uid = models.IntegerField()
    sid = models.IntegerField()
    mark = models.CharField(max_length=16, choices=MARKS)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def is_liked(cls, sid, uid):
        return cls.objects.filter(uid=sid, sid=uid,
                                  mark__in=['like', 'superlike']).exists()

    class Meta:
        db_table = 'swiped'
