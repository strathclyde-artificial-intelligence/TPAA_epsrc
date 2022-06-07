'use strict';

class View {

	constructor() {

		document.getElementById("runButton").addEventListener("click", this.getCode);
		document.getElementById("solutionBtn").addEventListener("click", this.showSolution);
		document.getElementById("nextButton").addEventListener("click", this.displayNextProblem);

	}

	showSolution(editor, solution) {
		editor.setValue(solution);
	}

	setSolutionHandler(listener) {
		document.getElementById("solutionBtn").addEventListener("click", listener);
	}

	setCode(editor, startingCode) {
		//let editor = document.getElementById("codeEditor");
		editor.setValue(startingCode);
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

	setUpNextProblemHandler(listener) {
		document.getElementById("nextButton").addEventListener("click", listener);
	}

	displayNextProblem() {
		document.getElementById("nextButtonContainer").style.display = "none";
	}

	showNextButton() {
		document.getElementById("nextButtonContainer").style.display = "flex";
	}

}
