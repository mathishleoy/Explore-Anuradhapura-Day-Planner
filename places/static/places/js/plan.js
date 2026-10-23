function getPlan() {
    return JSON.parse(localStorage.getItem('myDayPlan') || '[]');
}

function savePlan(plan) {
    localStorage.setItem('myDayPlan', JSON.stringify(plan));
    updateAddButtons();
}

function addToPlan(id) {
    const plan = getPlan();
    if (plan.includes(id)) return;
    plan.push(id);
    savePlan(plan);
}

function removeFromPlan(id) {
    savePlan(getPlan().filter(p => p !== id));
}

function updateAddButtons() {
    const plan = getPlan();
    document.querySelectorAll('[data-add-btn]').forEach(btn => {
        const id = parseInt(btn.dataset.addBtn);
        if (plan.includes(id)) {
            btn.textContent = 'Added';
            btn.classList.add('bg-terracotta-600', 'hover:bg-terracotta-700');
        } else {
            btn.textContent = 'Add';
            btn.classList.remove('bg-terracotta-600');
            btn.classList.add('bg-terracotta-700');
        }
    });
}

function moveStop(index, direction) {
    const plan = getPlan();
    const target = index + direction;
    if (target < 0 || target >= plan.length) return;
    [plan[index], plan[target]] = [plan[target], plan[index]];
    savePlan(plan);
    window.dispatchEvent(new Event('planChanged'));
}

document.addEventListener('DOMContentLoaded', updateAddButtons);
