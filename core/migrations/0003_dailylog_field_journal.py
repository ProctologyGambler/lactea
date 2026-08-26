from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_dailylog_breast_feeling_alter_dailylog_mood'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailylog',
            name='energy',
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[(1, 'Very low'), (2, 'Low'), (3, 'Moderate'), (4, 'Good'), (5, 'Great')],
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='dailylog',
            name='sleep_quality',
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[(1, 'Terrible'), (2, 'Poor'), (3, 'Okay'), (4, 'Good'), (5, 'Great')],
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='dailylog',
            name='hydration',
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[(1, 'Dehydrated'), (2, 'Could be better'), (3, 'Well hydrated')],
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='dailylog',
            name='stress',
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[(1, 'Very low'), (2, 'Low'), (3, 'Moderate'), (4, 'High'), (5, 'Very high')],
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='dailylog',
            name='tags',
            field=models.CharField(blank=True, help_text='Comma-separated custom tags', max_length=500),
        ),
    ]
