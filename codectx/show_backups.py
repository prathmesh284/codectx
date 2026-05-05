import json

backups = json.load(open('project.ctx.json.backup'))
print('BACKUP HISTORY (Sorted by analysis_time - Newest First):')
print(f'Total backups: {len(backups)}')
print()
for i, b in enumerate(backups):
    print(f'  Backup {i+1}: {b.get("analysis_time")}')
