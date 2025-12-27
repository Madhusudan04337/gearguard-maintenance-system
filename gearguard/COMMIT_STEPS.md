Per-app commit suggestions (run these after reviewing and staging changes):

- accounts:
  git add accounts
  git commit -m "feat(accounts): add management command to create initial superuser and basic templates"

- teams:
  git add teams
  git commit -m "style(teams): add basic Tailwind-ready templates and styles"

- equipment:
  git add equipment
  git commit -m "style(equipment): add basic Tailwind-ready templates and styles"

- maintenance:
  git add maintenance
  git commit -m "style(maintenance): add basic Tailwind-ready templates and styles"

- dashboard:
  git add dashboard
  git commit -m "style(dashboard): add base dashboard template and Tailwind layout"

- project root changes (settings, templates, tailwind files):
  git add gearguard/settings.py package.json tailwind.config.js postcss.config.js assets templates requirements.txt COMMIT_STEPS.md README_SETUP.md
  git commit -m "chore(project): configure PostgreSQL, static files and Tailwind build setup"
