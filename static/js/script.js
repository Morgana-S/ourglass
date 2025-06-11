const ratings = document.querySelectorAll('.review-rating');
const deleteButton = document.getElementById('confirm-delete');

/**
 * Ensures the DOM Content is loaded before executing functions
 */
document.addEventListener('DOMContentLoaded', function () {
	ratingsConverter();
	deleteButtonEnable();
	initializeTooltips();
	flatpickr('.flatpickr', {
		enableTime:  true,
		dateFormat: 'Y-m-d\\TH:i',
		locale: 'uk'
	})
});

/**
 * Converts the numerical value for user ratings into star icons from
 * FontAwesome
 */
function ratingsConverter() {
	ratings.forEach((element) => {
		const rating = parseInt(element.dataset.rating);
		let starsHtml = '';
		for (let i = 0; i < rating; i++) {
			starsHtml += "<i class='fa-solid fa-star text-warning'></i>";
		}
		element.innerHTML = starsHtml;
	});
}

function deleteButtonEnable() {
	if (deleteButton) {
		deleteButton.addEventListener('click', function () {
			document.getElementById('delete-form').submit();
		});
	}
}

function initializeTooltips(){
	const tooltipTriggerList = document.querySelectorAll(
		'[data-bs-toggle=tooltip]'
	);
	const tooltipList = [...tooltipTriggerList].map(
		(tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
	);
}