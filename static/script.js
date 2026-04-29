const yearSelect = document.getElementById("year-select");
const statusEl = document.getElementById("status");
const categoriesList = document.getElementById("categories-list");
const inducteesList = document.getElementById("inductees-list");

let selectedYear = "";
let selectedCategory = "";

function setStatus(message) {
	statusEl.textContent = message;
}

function populateYears(years) {
	yearSelect.innerHTML = "";

	const placeholder = document.createElement("option");
	placeholder.value = "";
	placeholder.textContent = "Select a year";
	placeholder.selected = true;
	yearSelect.appendChild(placeholder);

	years.forEach((year) => {
		const option = document.createElement("option");
		option.value = String(year);
		option.textContent = String(year);
		yearSelect.appendChild(option);
	});

	yearSelect.disabled = false;
}

function showEmptyInductees(message) {
	inducteesList.innerHTML = "";
	const emptyItem = document.createElement("li");
	emptyItem.className = "empty";
	emptyItem.textContent = message;
	inducteesList.appendChild(emptyItem);
}

function renderInductees(inductees, year, category) {
	inducteesList.innerHTML = "";

	if (!Array.isArray(inductees) || inductees.length === 0) {
		showEmptyInductees(`No inductees found in ${category} for ${year}.`);
		return;
	}

	inductees.forEach((name) => {
		const item = document.createElement("li");
		item.textContent = String(name);
		inducteesList.appendChild(item);
	});
}

async function loadInductees(year, category) {
	setStatus(`Loading inductees for ${category} (${year})...`);

	try {
		const response = await fetch(
			`/inductees?year=${encodeURIComponent(year)}&category=${encodeURIComponent(category)}`,
		);

		if (!response.ok) {
			throw new Error(`HTTP ${response.status}`);
		}

		const inductees = await response.json();
		renderInductees(inductees, year, category);
		setStatus(
			`Loaded ${inductees.length} inductee${inductees.length === 1 ? "" : "s"} in ${category} for ${year}.`,
		);
	} catch (error) {
		showEmptyInductees("Could not load inductees for the selected category.");
		setStatus("Could not load inductees. Please try another category.");
		console.error("Failed to load inductees", error);
	}
}

function renderCategories(categories, year) {
	categoriesList.innerHTML = "";
	selectedCategory = "";
	showEmptyInductees("Select a category to view its inductees.");

	if (!Array.isArray(categories) || categories.length === 0) {
		const emptyItem = document.createElement("li");
		emptyItem.className = "empty";
		emptyItem.textContent = `No categories found for ${year}.`;
		categoriesList.appendChild(emptyItem);
		showEmptyInductees(`No categories available for ${year}.`);
		return;
	}

	categories.forEach((category) => {
		const item = document.createElement("li");
		const button = document.createElement("button");
		button.type = "button";
		button.className = "category-btn";
		button.textContent = String(category);
		button.addEventListener("click", () => {
			selectedCategory = String(category);
			document.querySelectorAll("#categories-list li").forEach((li) => {
				li.classList.toggle("active", li === item);
			});
			loadInductees(selectedYear, selectedCategory);
		});
		item.appendChild(button);
		categoriesList.appendChild(item);
	});
}

async function loadCategoriesForYear(year) {
	setStatus(`Loading categories for ${year}...`);

	try {
		const response = await fetch(`/categories?year=${encodeURIComponent(year)}`);

		if (!response.ok) {
			throw new Error(`HTTP ${response.status}`);
		}

		const categories = await response.json();
		renderCategories(categories, year);
		setStatus(
			`Loaded ${categories.length} categor${categories.length === 1 ? "y" : "ies"} for ${year}.`,
		);
	} catch (error) {
		categoriesList.innerHTML = "";
		const errorItem = document.createElement("li");
		errorItem.className = "empty";
		errorItem.textContent = "Could not load categories for the selected year.";
		categoriesList.appendChild(errorItem);
		setStatus("Could not load categories. Please try another year.");
		console.error("Failed to load categories", error);
	}
}

async function loadYears() {
	setStatus("Requesting available years...");

	try {
		const response = await fetch("/years");

		if (!response.ok) {
			throw new Error(`HTTP ${response.status}`);
		}

		const years = await response.json();

		if (!Array.isArray(years) || years.length === 0) {
			yearSelect.innerHTML = '<option value="">No years available</option>';
			setStatus("No induction years were returned by the server.");
			return;
		}

		populateYears(years);
		setStatus(`Loaded ${years.length} year${years.length === 1 ? "" : "s"}.`);
	} catch (error) {
		yearSelect.innerHTML = '<option value="">Unable to load years</option>';
		setStatus("Could not load years. Please refresh and try again.");
		console.error("Failed to load years", error);
	}
}

yearSelect.addEventListener("change", (event) => {
	selectedYear = event.target.value;

	if (!selectedYear) {
		categoriesList.innerHTML = "";
		inducteesList.innerHTML = "";
		setStatus("Choose a year to load categories.");
		return;
	}

	loadCategoriesForYear(selectedYear);
});

loadYears();
