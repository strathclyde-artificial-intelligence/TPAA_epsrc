'use strict';

class Model {

	constructor() {

		this.problemObject;
		this.tokenObject;
		this.codeOutput;
	}

	fetchProblemObject(editor, problemNumber, setCode, setProblemStatement) {
		//fetching function for visiting currency
		let xhr = new XMLHttpRequest();
		const that = this;
		if(problemNumber == null) {
			//if the number has not been set or cleared we fetch the first problem
			problemNumber = "One";
		}

		xhr.addEventListener("load", function() {
			let text = this.responseText;
			let jsonObj = JSON.parse(text);
			that.setProblemObject(jsonObj);
			view.setCode(editor, jsonObj.code);
			view.setProblemStatement(jsonObj.statement);
			view.displayProblemText();
			view.changeActiveButton("Problem");
		});

		let URL = "index.php/?func="+problemNumber;
		xhr.open("GET", URL, true);
		xhr.send();
	}

	setLocalStorage(nameOfCurrentProblem) {
		console.log(nameOfCurrentProblem);
		localStorage.setItem("currentProblem", nameOfCurrentProblem);
	}

	setLocalStorage(nameOfCurrentProblem) {
		console.log(nameOfCurrentProblem);
		localStorage.setItem("currentProblem", nameOfCurrentProblem);

	}

	sendCodeRequest(codeRan, setCodeOutputBox, removeLoadingAnimation, testString) {
		
		let combinedCode = codeRan + testString;
		let newData = btoa(combinedCode);

		let xhr = new XMLHttpRequest();
		const that = this;

		xhr.addEventListener("load", function() {
			let text = this.responseText;
			let jsonObj = JSON.parse(text);
			console.log(jsonObj);
			that.fetchCodeResult(jsonObj.token, setCodeOutputBox, removeLoadingAnimation);
		});

		let URL = "send.php/?code="+newData;
		xhr.open("GET", URL, true);
		xhr.send();

	}

	setTokenObject(tokenReceived) {
		this.tokenObject = tokenReceived;
	}

	fetchCodeResult(token, setCodeOutputBox, removeLoadingAnimation) {
		
		const that = this;
		let xhr = new XMLHttpRequest();

		xhr.addEventListener("readystatechange", function() {
			if(this.readyState == this.DONE) {
				let collectedData = this.responseText;
				let data = JSON.parse(collectedData);
				console.log(data);
				if(data.stdout === null) {
					view.removeLoadingAnimation();
					view.setCodeOutputBox("error");
				} else {
					that.setProblemOutput(atob(data.stdout));
					view.removeLoadingAnimation();
					view.setCodeOutputBox(atob(data.stdout));
				}
			}
		});

		let URL = "getCode.php/?token="+token;
		xhr.open("GET", URL, true);
		xhr.send();
	}

	setProblemObject(jsonObj) {
		this.problemObject = jsonObj;
	}

	setProblemOutput(output) {
		this.codeOutput = output;
	}

	getProblemOutput() {
		return this.codeOutput;
	}

	getProblemObject() {
		return this.problemObject;
	}
}
