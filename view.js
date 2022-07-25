'use strict';

class View {

	constructor() {

		document.getElementById("runButton").addEventListener("click", this.getCode);
		document.getElementById("nextButton").addEventListener("click", this.displayNextProblem);
		document.getElementById("tabOptionProblem").addEventListener("click", this.displayProblemText);
		document.getElementById("tabOptionSolution").addEventListener("click", this.displaySolutionText);

	}

	showSolution(solution, changeActiveButton) {
		let solutionText = document.getElementById("solutionParagraph");
		solutionText.innerText = solution;
		view.changeActiveButton("Solution")
	}

	setSolutionHandler(listener) {
		document.getElementById("tabOptionSolution").addEventListener("click", listener);
	}

	setCode(editor, startingCode) {
		//let editor = document.getElementById("codeEditor");
		editor.setValue(startingCode);
	}

	setCodeOutputBox(output) {
		let outputBox = document.getElementById("codeOutput");
		outputBox.innerText = output;
	}

	setProblemStatement(problemText) {
		let problem = document.getElementById("problemParagraph");
		problem.innerText = problemText;

	}

	setUpProblemEvaluationHandler(listener) {
		document.getElementById("runButton").addEventListener("click", listener);
	}

	clearEditor(editor) {
		let clear = "";
		//function from codemirror, sets value in editor
		editor.setValue(clear);
	}
	
	getCode(editor) {
		//function from codemirror, gets value from editor
		let code = editor.getValue();
		return code;
	}


	removeSubmitButton() {
		let submitButton = document.getElementById("submitButton");
		submitButton.setAttribute("hidden", "hidden");
	}

	activateSubmitButton() {
		let submitButton = document.getElementById("submitButton");
		let hidden = submitButton.getAttribute("hidden");
		if(hidden) {
			submitButton.removeAttribute("hidden");
		}
	}

	activateRunButton() {
		let runButton = document.getElementById("runButton");
		runButton.disable = false;
	}

	deactivateRunButton() {
		let runButton = document.getElementById("runButton");
		runButton.disable = true;
	}

	setUpNextProblemHandler(listener) {
		document.getElementById("nextButton").addEventListener("click", listener);
	}

	setUpSubmitHandler(listener) {
		document.getElementById("submitButton").addEventListener("click", listener);
	}

	displayNextProblem() {
		document.getElementById("nextButtonContainer").style.display = "none";
	}

	displayProblemText() {
		document.getElementById("tabSolutionText").style.display = "none";
		document.getElementById("tabProblemText").style.display = "flex";
	}
	
	displaySolutionText() {
		document.getElementById("tabProblemText").style.display = "none";
		document.getElementById("tabSolutionText").style.display = "flex";
	}

	showNextButton() {
		document.getElementById("nextButtonContainer").style.display = "flex";
	}

	setProblemTabHandler(listener) {
		document.getElementById("tabOptionProblem").addEventListener("click", listener);

	}

	showLoadingAnimation() {
		document.getElementById("loader").style.display = "flex";
	}

	removeLoadingAnimation() {
		document.getElementById("loader").style.display = "none";
	}

	setOutputText(code) {
		let output = document.getElementById("codeOutput");
		output.innerText = code;
	}

	clearCodeoutput() {
		document.getElementById("codeOutput").innerHTML = "";
	}

	changeActiveButton(change) {
		//set the correct tabButton to be active
		let element = document.getElementsByClassName("tabOption");

		for(let i = 0; i < element.length; i++) {
			if(element[i].value == change) {
				element[i].className = element[i].className.replace(" active", "");
				element[i].className +=" active";
			} else {
				element[i].className = element[i].className.replace(" active", "");
			}
		}
	}
}
