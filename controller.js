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
		console.log(code);
		let solutionObject = model.getProblemObject();
		model.sendCodeRequest(code, view.setOutputBox, view.removeLoadingAnimation, solutionObject.testCases);

	});

	view.setUpSubmitHandler(() => {
		let solutionObject = model.getProblemObject();
		let outputCode = model.getProblemOutput();
		//if code has not been run, outputCode object will be undefined so we have to check this
		if(outputCode == undefined) {
			view.setOutputText("Before you submit your code make sure to run it.");
		} else {
			let cleanSolutionText = solutionObject.testOutput.replace(/^[0-9\s]*|[+*\r\n]/g, "")
			let cleanOutpuText = outputCode.replace(/^[0-9\s]*|[+*\r\n]/g, "");

			if (cleanSolutionText == cleanOutpuText) {

				view.setOutputText("Correct");
				let currentIndex = numbers.indexOf(currentProblem);

				if(currentIndex < 4) { 
					model.setLocalStorage(numbers[currentIndex+1]);
					view.showNextButton();
				}
				//reset to the first problem if we have come to a last problem and made it will
				if(currentIndex == 4) {
					view.setOutputText("Correct");
					model.setLocalStorage("One");
					view.showNextButton();
				}
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
