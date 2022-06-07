'use strict';

class Model {

	constructor() {

		this.problemObject;

	}

	fetchProblemObject(editor, problemNumber, setCode, setProblemStatement) {
		//fetching function for visiting currency
		let xhr = new XMLHttpRequest();
		const that = this;
		if(currentProblem == null) {
			//if the number has not been set or cleared we fetch the first problem
			problemNumber = numbers[0];
		}

		xhr.addEventListener("load", function() {
			let text = this.responseText;
			let jsonObj = JSON.parse(text);
			that.setProblemObject(jsonObj);
			view.setCode(editor, jsonObj.code);
			view.setProblemStatement(jsonObj.statement);
		});

		let URL = "http://localhost:8888/index.php/?func="+problemNumber;
		xhr.open("GET", URL, true);
		xhr.send();
	}

	setLocalStorage(nameOfCurrentProblem) {
		console.log(nameOfCurrentProblem);
		localStorage.setItem("currentProblem", nameOfCurrentProblem);
	}

	setProblemObject(jsonObj) {
		this.problemObject = jsonObj;
	}

	getProblemObject() {
		return this.problemObject;
	}
}
