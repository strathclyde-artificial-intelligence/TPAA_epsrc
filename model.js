'use strict';

class Model {

	constructor() {

		this.problemObject;
		this.tokenObject;
		this.codeOutput;
		this.solutionOutput;
		this.batchedSolutions = {};
		this.tries = {};
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
			that.sendSolutionRequest(jsonObj.testCase, jsonObj.testCaseStr)
			let testCases = jsonObj.testCases;
			let typeOfRequest = "solution";
			
			for(let i = 0; i < testCases.length; i++) {
				that.sendBatchRequest(jsonObj.testCase, testCases[i], i, typeOfRequest);
			}
			view.changeActiveButton("Problem");
		});

		let URL = "index.php";
		xhr.open("GET", URL, true);
		xhr.send();
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

	sendCodeRequest(codeRan, setCodeOutputBox, activateSubmitButton, activateRunButton, removeLoadingAnimation, testString) {
		
		this.batchedTries = {};
		let combinedCode = codeRan + '\n' + testString;
		let newData = btoa(combinedCode);

		let xhr = new XMLHttpRequest();
		const that = this;

		xhr.addEventListener("load", function() {
			let text = this.responseText;
			let jsonObj = JSON.parse(text);
			that.fetchCodeResult(codeRan, jsonObj.token, setCodeOutputBox, activateSubmitButton, activateRunButton, removeLoadingAnimation);
		});

		let URL = "send.php/?code="+newData;
		xhr.open("GET", URL, true);
		xhr.send();

	}

	fetchCodeResult(codeRan, token, setCodeOutputBox, activateSubmitButton, activateRunButton, removeLoadingAnimation) {
		
		const that = this;
		let xhr = new XMLHttpRequest();

		xhr.addEventListener("readystatechange", function() {
			if(this.readyState == this.DONE) {
				let collectedData = this.responseText;
				let data = JSON.parse(collectedData);
				if(data.stdout === null) {
					view.removeLoadingAnimation();
					view.setCodeOutputBox("Error");
				} else {
					that.setProblemOutput(atob(data.stdout));
					view.removeLoadingAnimation();
					let output = that.getSolutionOutput();
					let outputStr = `Output = ${atob(data.stdout)}\nExpected = ${output}`
					view.setCodeOutputBox(outputStr);
					let solutionObject = that.getProblemObject();
					let testCases = solutionObject.testCases;
					let typeOfRequest = "tries";
					for(let i = 0; i < testCases.length; i++) {
						that.sendBatchRequest(codeRan, testCases[i], i, typeOfRequest);
					}
					if(output == atob(data.stdout)) {
						view.activateSubmitButton();
					}
				}
					view.activateRunButton();
			}
		});

		let URL = "getCode.php/?token="+token;
		xhr.open("GET", URL, true);
		xhr.send();
	}

	sendBatchRequest(startingCode, testCase, index, typeOfRequest) {
		
		let newData = startingCode + '\n' + testCase;
		let code = btoa(newData);

		let xhr = new XMLHttpRequest();
		const that = this;

		xhr.addEventListener("load", function() {
			let text = this.responseText;
			let jsonObj = JSON.parse(text);
			that.fetchBatchResult(jsonObj.token, index, typeOfRequest);
		});

		let URL = "send.php/?code="+code;
		xhr.open("GET", URL, true);
		xhr.send();

	}

	fetchBatchResult(token, index, typeOfRequest) {

		const that = this;
		let xhr = new XMLHttpRequest();

		xhr.addEventListener("readystatechange", function() {
			if(this.readyState == this.DONE) {
				let collectedData = this.responseText;
				let data = JSON.parse(collectedData);
				if(typeOfRequest == "solution") {
					that.setBatchedSolutions(atob(data.stdout), index);
				} else if (typeOfRequest == "tries") {
					that.setBatchedTries(atob(data.stdout), index);
				}
			}
		});

		let URL = "getCode.php/?token="+token;
		xhr.open("GET", URL, true);
		xhr.send();
	}
	
	setTokenObject(tokenReceived) {
		this.tokenObject = tokenReceived;
	}

	setSolutionOutput(testCase) {
		this.solutionOutput = testCase;
	}

	setBatchedTries(testCase, index) {
		this.batchedTries[index] = testCase;
	}

	setBatchedSolutions(testCase, index) {
		this.batchedSolutions[index] = testCase;
	}

	setProblemObject(jsonObj) {
		this.problemObject = jsonObj;
	}

	setProblemOutput(output) {
		this.codeOutput = output;
	}

	getBatchedTries() {
		return this.batchedTries;
	}

	getBatchedSolutions() {
		return this.batchedSolutions;
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
