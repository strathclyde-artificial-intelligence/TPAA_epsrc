let model, view;
let currentProblem = localStorage.getItem("currentProblem");

const initalise = evt => {
	
	model = new Model();
	view = new View();
	//definition of editor, codemirror library use
	let editor = CodeMirror.fromTextArea(
		document.getElementById("codeEditor"),
		{
			smartIndent: false, 
			lineNumbers: true,
			electricChars: false, 
			indentWithTabs: false, 
			indentUnit: 4, 
			extraKeys: {Tab: "indentMore"}, 
			mode: null, 
		}
	  );

	//fetch problem from php
	model.fetchProblemObject(editor, currentProblem, view.setCode, view.setProblemStatement, view.displayProblemText, view.changeActiveButton);
	
	view.setUpProblemEvaluationHandler(() => {

		view.removeSubmitButton();
		view.deactivateRunButton();
		//we clear the output for loading animation
		view.setCodeOutputBox("");
		view.showLoadingAnimation();
		let code = view.getCode(editor);
		let solutionObject = model.getProblemObject();

		model.sendCodeRequest(code, view.setOutputBox, view.activateSubmitButton, view.activateRunButton, view.removeLoadingAnimation, solutionObject.testCaseStr);

	});

	view.setUpSubmitHandler(() => {

		let solutionCases = model.getBatchedSolutions();
		let actualCases = model.getBatchedTries();
		let outputCode = model.getProblemOutput();

		let len = Object.keys(solutionCases).length;
		let outputStr = "";
		let areEqual = true;

		for(let i = 0; i < len; i++) {
			if(actualCases[i] != solutionCases[i]) {
				areEqual = false;
			}
			outputStr += `${i+1}:Output = ${actualCases[i]}${i+1}:Expected = ${solutionCases[i]}\n`;
		}

		if(outputCode == undefined) {
			view.setOutputText("Before you submit your code make sure to run it.");
		} else {
			if (areEqual) {
				view.setOutputText("Correct\n" + outputStr);
				view.showNextButton();
			} else {
				view.setOutputText(outputStr);
			}
		}
		view.activateSubmitButton();
		view.activateRunButton();
	});

	view.setUpNextProblemHandler(() => {
		location.reload();
	});


	view.setProblemTabHandler(() => {
		let solutionObject = model.getProblemObject();
		view.setProblemStatement(solutionObject.statement);
		view.changeActiveButton("Problem");
		view.displayProblemText();

	});
	
	view.setSolutionHandler(() => {
		let solutionObject = model.getProblemObject();
		view.showSolution(solutionObject.solution, view.changeActiveButton);

	});
}

window.addEventListener("load", initalise);
