from django.db import migrations

def resolve_duplicates(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    duplicates = ['amine@gmail.com', 'yassine@gmail.com', 'yassinealahyane6@gmail.com']
    
    for email in duplicates:
        users = User.objects.filter(email=email).order_by('id')
        for i, user in enumerate(users[1:]):
            user.email = f"{email.split('@')[0]}+dup{i+1}@{email.split('@')[1]}"
            user.save()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0003_candidate_profession'),
    ]
    operations = [
        migrations.RunPython(resolve_duplicates),
    ]