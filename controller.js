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
			
		//we clear the output for loading animation
		view.setCodeOutputBox("");
		view.showLoadingAnimation();
		let code = view.getCode(editor);
		let solutionObject = model.getProblemObject();
		model.sendSolutionRequest(solutionObject.testCase, solutionObject.testCaseStr);
		model.sendCodeRequest(code, view.setOutputBox, view.removeLoadingAnimation, solutionObject.testCaseStr);
		

	});

	view.setUpSubmitHandler(() => {
		let outputCode = model.getProblemOutput();
		let solutionCode = model.getSolutionOutput();

		if(outputCode == undefined) {
			view.setOutputText("Before you submit your code make sure to run it.");
		} else {

			if (outputCode == solutionCode) {
				view.setOutputText("Correct");
				view.showNextButton();
			} else {
				view.setOutputText("Incorrect answer.");
			}
		}

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
