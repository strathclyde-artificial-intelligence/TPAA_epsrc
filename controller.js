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

	model.fetchProblemObject(editor, currentProblem, view.setCode, view.setProblemStatement, view.displayProblemText, view.changeActiveButton);
	
	view.setUpProblemEvaluationHandler(() => {
		let code = view.getCode(editor);
		/*after this we need to check the model if this is the correct code
		 * We need to pass the problem and what language it is in order to get the proper solution
		 * preferably we run the code remotely in some container and then check result:
		 * right now we are just looking at the actual string and comparing it to solution
		 */
		let solutionObject = model.getProblemObject();

		if (solutionObject.solution == code) {

			//should insert the output from token judge0, for now filler text
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

		} else {
			//should insert the output from token judge0, for now filler text
			view.setOutputText("Incorrect");
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
