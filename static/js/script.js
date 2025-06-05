document.addEventListener('DOMContentLoaded', function () {
	const ratings = document.querySelectorAll('.review-rating');

	ratings.forEach(function (element) {
		const rating = parseInt(element.dataset.rating);
		let starsHtml = '';
		for (let i = 0; i < rating; i++) {
			starsHtml += "<i class='fa-solid fa-star text-warning'></i>";
		}
		element.innerHTML = starsHtml;
	});
});
