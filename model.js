'use strict';

class Model {

	constructor() {

		this.problemObject;
		this.tokenObject;
		this.codeOutput;
		this.solutionOutput
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

		let URL = "index.php";
		xhr.open("GET", URL, true);
		xhr.send();
	}

	setLocalStorage(nameOfCurrentProblem) {
		localStorage.setItem("currentProblem", nameOfCurrentProblem);
	}

	setLocalStorage(nameOfCurrentProblem) {
		localStorage.setItem("currentProblem", nameOfCurrentProblem);

	}

	sendSolutionRequest(solutionCode, runStr) {

		
		let test = solutionCode + '\n' + runStr;
		let newData = btoa(test);

		let xhr = new XMLHttpRequest();
		const that = this;

		xhr.addEventListener("load", function() {
			let text = this.responseText;
			let jsonObj = JSON.parse(text);
			that.fetchSolutionResult(jsonObj.token);
		});

		let URL = "send.php/?code="+newData;
		xhr.open("GET", URL, true);
		xhr.send();

	}

	setTokenObject(tokenReceived) {
		this.tokenObject = tokenReceived;
	}

	fetchSolutionResult(token) {
		
		const that = this;
		let xhr = new XMLHttpRequest();

		xhr.addEventListener("readystatechange", function() {
			if(this.readyState == this.DONE) {
				let collectedData = this.responseText;
				let data = JSON.parse(collectedData);
				that.setSolutionOutput(atob(data.stdout));
			}
		});

		let URL = "getCode.php/?token="+token;
		xhr.open("GET", URL, true);
		xhr.send();
	}

	sendCodeRequest(codeRan, setCodeOutputBox, removeLoadingAnimation, testString) {
		
		let combinedCode = codeRan + '\n' + testString;
		let newData = btoa(combinedCode);

		let xhr = new XMLHttpRequest();
		const that = this;

		xhr.addEventListener("load", function() {
			let text = this.responseText;
			let jsonObj = JSON.parse(text);
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

	setSolutionOutput(solutionOutput) {
		this.solutionOutput = solutionOutput

	}

	setProblemObject(jsonObj) {
		this.problemObject = jsonObj;
	}

	setProblemOutput(output) {
		this.codeOutput = output;
	}

	getSolutionOutput() {
		return this.solutionOutput;
	}
	getProblemOutput() {
		return this.codeOutput;
	}

	getProblemObject() {
		return this.problemObject;
	}
}
