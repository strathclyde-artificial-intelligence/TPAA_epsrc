let model, view;
let currentProblem = localStorage.getItem("currentProblem");

const initalise = evt => {
	//array of strings used for fetching from index.php
	let numbers = ["One", "Two", "Three", "Four", "Five"];
	
	model = new Model();
	view = new View();
	//definition of editor, codemirror library use
	let editor = CodeMirror.fromTextArea(
		document.getElementById("codeEditor"),
		{
			lineNumbers: true,
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
		//if code has not been run, outputCode object will be undefined so we have to check this
		let test = model.getSolutionOutput();

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
