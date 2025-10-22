#!/bin/bash

# Git Flow Helper Script
# Ayuda a gestionar el flujo de trabajo con branches feature/fix

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Función para crear una nueva feature branch
create_feature() {
    local feature_name=$1

    if [ -z "$feature_name" ]; then
        print_error "Debes proporcionar un nombre para la feature"
        echo "Uso: $0 feature <nombre-de-la-feature>"
        exit 1
    fi

    # Asegurarse de estar en dev actualizado
    print_info "Cambiando a branch dev..."
    git checkout dev

    print_info "Actualizando dev desde origin..."
    git pull origin dev

    # Crear nueva feature branch
    local branch_name="feature/$feature_name"
    print_info "Creando branch $branch_name..."
    git checkout -b "$branch_name"

    print_success "Feature branch '$branch_name' creada exitosamente"
    print_info "Ahora puedes trabajar en tu feature. Cuando termines, usa:"
    echo "  git add ."
    echo "  git commit -m 'tu mensaje'"
    echo "  ./scripts/git-flow-helper.sh merge-to-dev"
}

# Función para crear una nueva fix branch
create_fix() {
    local fix_name=$1

    if [ -z "$fix_name" ]; then
        print_error "Debes proporcionar un nombre para el fix"
        echo "Uso: $0 fix <nombre-del-fix>"
        exit 1
    fi

    # Asegurarse de estar en dev actualizado
    print_info "Cambiando a branch dev..."
    git checkout dev

    print_info "Actualizando dev desde origin..."
    git pull origin dev

    # Crear nueva fix branch
    local branch_name="fix/$fix_name"
    print_info "Creando branch $branch_name..."
    git checkout -b "$branch_name"

    print_success "Fix branch '$branch_name' creada exitosamente"
    print_info "Ahora puedes trabajar en tu fix. Cuando termines, usa:"
    echo "  git add ."
    echo "  git commit -m 'tu mensaje'"
    echo "  ./scripts/git-flow-helper.sh merge-to-dev"
}

# Función para mergear feature/fix a dev
merge_to_dev() {
    local current_branch=$(git branch --show-current)

    # Verificar que estemos en una feature o fix branch
    if [[ ! $current_branch =~ ^(feature|fix)/ ]]; then
        print_error "Debes estar en una feature o fix branch"
        print_info "Branch actual: $current_branch"
        exit 1
    fi

    print_info "Verificando que no haya cambios sin commitear..."
    if ! git diff-index --quiet HEAD --; then
        print_error "Tienes cambios sin commitear. Por favor haz commit primero."
        exit 1
    fi

    print_info "Pusheando branch actual a origin..."
    git push -u origin "$current_branch"

    print_info "Cambiando a branch dev..."
    git checkout dev

    print_info "Actualizando dev desde origin..."
    git pull origin dev

    print_info "Mergeando $current_branch a dev..."
    git merge --no-ff "$current_branch" -m "Merge branch '$current_branch' into dev"

    print_info "Pusheando dev a origin..."
    git push origin dev

    print_success "Branch '$current_branch' mergeada exitosamente a dev"

    print_warning "¿Quieres eliminar la branch '$current_branch'? (y/n)"
    read -r response
    if [ "$response" = "y" ]; then
        git branch -d "$current_branch"
        git push origin --delete "$current_branch"
        print_success "Branch '$current_branch' eliminada"
    fi
}

# Función para mergear dev a main
merge_to_main() {
    local current_branch=$(git branch --show-current)

    # Verificar que estemos en dev
    if [ "$current_branch" != "dev" ]; then
        print_warning "No estás en la branch dev. Cambiando..."
        git checkout dev
    fi

    print_info "Actualizando dev desde origin..."
    git pull origin dev

    print_warning "¿Estás seguro de mergear dev a main? Esto debería hacerse solo cuando el código está listo para producción. (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        print_info "Merge cancelado"
        exit 0
    fi

    print_info "Cambiando a branch main..."
    git checkout main

    print_info "Actualizando main desde origin..."
    git pull origin main

    print_info "Mergeando dev a main..."
    git merge --no-ff dev -m "Merge branch 'dev' into main - Production release"

    print_info "Pusheando main a origin..."
    git push origin main

    print_success "Dev mergeada exitosamente a main"
    print_info "Ahora puedes deployar a Railway"

    git checkout dev
}

# Función para mostrar el status del flujo
show_status() {
    local current_branch=$(git branch --show-current)

    echo ""
    print_info "=== Git Flow Status ==="
    echo ""
    print_info "Branch actual: $current_branch"
    echo ""

    print_info "Branches locales:"
    git branch
    echo ""

    print_info "Cambios pendientes:"
    git status -s
    echo ""

    print_info "Últimos commits en $current_branch:"
    git log --oneline -5
    echo ""
}

# Función para crear hotfix
create_hotfix() {
    local hotfix_name=$1

    if [ -z "$hotfix_name" ]; then
        print_error "Debes proporcionar un nombre para el hotfix"
        echo "Uso: $0 hotfix <nombre-del-hotfix>"
        exit 1
    fi

    # Asegurarse de estar en main actualizado
    print_info "Cambiando a branch main..."
    git checkout main

    print_info "Actualizando main desde origin..."
    git pull origin main

    # Crear nueva hotfix branch
    local branch_name="hotfix/$hotfix_name"
    print_info "Creando branch $branch_name..."
    git checkout -b "$branch_name"

    print_success "Hotfix branch '$branch_name' creada exitosamente"
    print_warning "Los hotfixes son para emergencias. Cuando termines:"
    echo "  1. Haz commit de tus cambios"
    echo "  2. Mergea a main: git checkout main && git merge $branch_name"
    echo "  3. Mergea a dev: git checkout dev && git merge $branch_name"
    echo "  4. Elimina la branch: git branch -d $branch_name"
}

# Main script
case "$1" in
    feature)
        create_feature "$2"
        ;;
    fix)
        create_fix "$2"
        ;;
    hotfix)
        create_hotfix "$2"
        ;;
    merge-to-dev)
        merge_to_dev
        ;;
    merge-to-main)
        merge_to_main
        ;;
    status)
        show_status
        ;;
    *)
        echo "Git Flow Helper - Gestión de branches para el proyecto"
        echo ""
        echo "Uso: $0 <comando> [argumentos]"
        echo ""
        echo "Comandos:"
        echo "  feature <nombre>     - Crear nueva feature branch desde dev"
        echo "  fix <nombre>         - Crear nueva fix branch desde dev"
        echo "  hotfix <nombre>      - Crear nueva hotfix branch desde main"
        echo "  merge-to-dev         - Mergear branch actual a dev"
        echo "  merge-to-main        - Mergear dev a main (producción)"
        echo "  status               - Mostrar status del flujo actual"
        echo ""
        echo "Ejemplos:"
        echo "  $0 feature user-authentication"
        echo "  $0 fix login-validation"
        echo "  $0 merge-to-dev"
        echo "  $0 merge-to-main"
        echo "  $0 status"
        exit 1
        ;;
esac
