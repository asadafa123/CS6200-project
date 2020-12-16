from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from Insta.serializers import Blog, ElasticBlogSerializer

@receiver(pre_save, sender=Blog, dispatch_uid="update_record")
def update_es_record(sender, instance, **kwargs):
    obj = ElasticBlogSerializer(instance)
    obj.save()

@receiver(post_delete, sender=Blog, dispatch_uid="delete_record")
def delete_es_record(sender, instance, *args, **kwargs):
    obj = ElasticBlogSerializer(instance)
    obj.delete(ignore=404)