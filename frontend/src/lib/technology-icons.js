const ICONS = {
  python: 'py.svg',
  django: 'dj.svg',
  'django rest framework': 'dj.svg',
  fastapi: 'fastapi.svg',
  postgresql: 'postgresql.svg',
  mysql: 'mysql.svg',
  docker: 'docker.svg',
  git: 'git.svg',
  github: 'Github_light.svg',
  linux: 'linux.svg',
  jwt: 'jwt.svg',
  react: 'react.svg',
  vite: 'javascript.svg',
  'tailwind css': 'tailwindcss.svg',
  javascript: 'javascript.svg',
}

export function technologyIcon(name) {
  const normalized = name?.trim().toLowerCase()
  const filename = ICONS[normalized]
  return filename ? `/svg/${filename}` : null
}
