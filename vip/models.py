from django.db import models


class Vip(models.Model):
    """
    会员
    """
    name = models.CharField(max_length=32, unique=True)
    level = models.IntegerField(unique=True, default=0)
    # price decimal(5,2)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    @property
    def perms(self):
        """
        vip， 所应的权限
        :return:
        """
        if not hasattr(self, '_perms'):
            # 通过 vip 权限 关系表获得 vip 对应的 权限id
            vip_perms = VipPermission.objects.filter(vip_id=self.id).only('perm_id')
            perm_id_list = [p.perm_id for p in vip_perms]
            # 通过权限id 获得 权限
            perms = Permission.objects.filter(id__in=perm_id_list).only('name')
            self._perms = perms

        return self._perms

    def has_perm(self, perm_name):
        """
        检查当前vip等级是否拥有某种权限
        :param perm_name:
        :return:
        """

        perm_names = [p.name for p in self.perms]

        return perm_name in perm_names

    class Meta:
        db_table = 'vips'


class Permission(models.Model):
    """
    权限
    """
    name = models.CharField(max_length=32, unique=True)
    description = models.TextField()

    class Meta:
        db_table = 'permissions'


class VipPermission(models.Model):
    """
    会员-权限 关系
    """
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()

    class Meta:
        db_table = 'vip_permissions'
