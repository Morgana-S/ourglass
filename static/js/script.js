/**
 * Ensures the DOM Content is loaded before executing functions
 */
document.addEventListener('DOMContentLoaded', function () {
	ratingsConverter();
	document.getElementById('confirm-delete-button').addEventListener('click', deleteEvent);
});

/**
 * Converts the numerical value for user ratings into star icons from
 * FontAwesome
 */
function ratingsConverter() {
	const ratings = document.querySelectorAll('.review-rating');
	ratings.forEach((element) => {
		const rating = parseInt(element.dataset.rating);
		let starsHtml = '';
		for (let i = 0; i < rating; i++) {
			starsHtml += "<i class='fa-solid fa-star text-warning'></i>";
		}
		element.innerHTML = starsHtml;
	});
}

function deleteEvent(){
	document.getElementById('delete-event-form').submit();
}