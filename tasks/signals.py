from django.db.models.signals import (
    m2m_changed,
    pre_save,
    post_save,
    pre_delete,
    post_delete,
)
from django.dispatch import receiver

from tasks.models import (
    TodoItem,
    Category,
    PriorityCounter,
)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_preadded(sender, instance, action, model, **kwargs):
    if action != "pre_add":
        return

    for cat in instance.category.all():
        new_count = cat.todos_count - 1
        Category.objects.filter(slug=cat.slug).update(todos_count=new_count)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, **kwargs):
    if action != "post_add":
        return

    for cat in instance.category.all():
        new_count = cat.todos_count + 1
        Category.objects.filter(slug=cat.slug).update(todos_count=new_count)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_preremoved(sender, instance, action, model, **kwargs):
    if action != "pre_remove":
        return

    for cat in instance.category.all():
        new_count = cat.todos_count - 1
        Category.objects.filter(slug=cat.slug).update(todos_count=new_count)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_removed(sender, instance, action, model, **kwargs):
    if action != "post_remove":
        return

    for cat in instance.category.all():
        new_count = cat.todos_count + 1
        Category.objects.filter(slug=cat.slug).update(todos_count=new_count)


@receiver(pre_delete, sender=TodoItem)
def task_cats_delete(sender, instance, **kwargs):
    for cat in instance.category.all():
        cat.todos_count -= 1
        cat.save()


@receiver(pre_save, sender=TodoItem)
def priority_counter_preadded(sender, instance, **kwargs):
    if instance.id is None:
        pass
    else:
        previous = TodoItem.objects.get(id=instance.id)
        previous_counter = PriorityCounter.objects.filter(priority=previous.priority).first()
        previous_counter.counter -= 1
        previous_counter.save()


@receiver(post_save, sender=TodoItem)
def priority_counter_added(sender, instance, **kwargs):
    instance.priority_counter, created = PriorityCounter.objects.get_or_create(priority=instance.priority)
    instance.priority_counter.counter += 1
    instance.priority_counter.save()


@receiver(post_delete, sender=TodoItem)
def priority_counter_deleted(sender, instance, **kwargs):
    active = PriorityCounter.objects.filter(priority=instance.priority).first()
    active.counter -= 1
    active.save()

