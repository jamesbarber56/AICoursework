import java.util.HashSet;
import java.io.File;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Set;
import java.util.Stack;

enum moveDir{
	//enumerator that has constants for each direction
	UP,
	DOWN,
	LEFT,
	RIGHT;
}

public class TileProblem {	
	public static void main(String[] args) {	
		//gets the strings from the input into the console then runs the algorithm on them.
		runAlgorithm(args[0], args[1]);
	}
	
	static void runAlgorithm(String S1, String S2) {
		tileStates RS1 = new tileStates(S1); //Initialises the problem for each given start states
		tileStates RS2 = new tileStates(S2);
		RS1.stackAlgorithm(); //runs the algorithm on each states
		RS2.stackAlgorithm();
		System.out.print("States in RS1: "); //prints information into the console about the sizes
		System.out.println(RS1.RS);
		System.out.print("States in RS2: ");
		System.out.println(RS2.RS);
		outputToFile(RS1, RS2); //outputs the sets into the their respective files
		int RS1RS2= compareSets(RS1, RS2);
		System.out.print("States in RS1 but not in RS2 (RS1/RS2): ");
		System.out.println(RS1RS2);
	}
	
	static int compareSets(tileStates RS1, tileStates RS2) {
		//compares the two sets
		int ammountInBoth = 0;
		for(String state : RS1.states) { //for each state in rs1
			if(!RS2.states.contains(state)) { //check if its in rs2
				ammountInBoth++; //if it isnt in rs1 then add one
			}
		}
		return ammountInBoth;
	}
	
	static void outputToFile(tileStates RS1, tileStates RS2) {
		try {
			//creates a buffered writer so i can write strings, for each set of states
			File rs1f = new File("./rs1.txt");
			File rs2f = new File("./rs2.txt");
			BufferedWriter rs1 = new BufferedWriter(new FileWriter(rs1f));
			BufferedWriter rs2 = new BufferedWriter(new FileWriter(rs2f));
			rs1.write(RS1.states.toString()); //writes a string version of the set to file
			rs2.write(RS2.states.toString());
			rs1.flush();
			rs2.flush();
			rs1.close();//closes the files
			rs2.close();
		} catch (IOException e) {
			System.out.println("File Not found");//incase of any IO error
			e.printStackTrace();
		}
		
		
		
	}
	
}


class tileStates {
	//Object for holding all the states and the number of states in each set.
	//using hash set as any duplicates would not be added, no need for additional validation
	Set<String> states; //states in the set
	int RS; //ammount of states in set
	State root; // stored root state;
	tileStates(String tile){
		states = new HashSet<>(); //initilize hash set with nothing in	
		this.root = new State(tile);
		this.RS = 0; //doesn't include root as its one or more moves to add
	}
	
	void stackAlgorithm(){
		//this is the stake algorithm that i explained in the written document
		Stack<State> statesToExplore = new Stack<>(); //create a stack to push and pip from
		State currentState;
		
		statesToExplore.push(this.root);//pushes the root state onto the stack
		while(!statesToExplore.empty()) { //whilst stack isnt empty, carry on
			currentState = statesToExplore.pop();//pop the state thats on the top of the stack
			String down = currentState.moveBlank(moveDir.DOWN); //make each direction that can come off that state
			String up = currentState.moveBlank(moveDir.UP);
			String left = currentState.moveBlank(moveDir.LEFT);
			String right = currentState.moveBlank(moveDir.RIGHT);
			if(!states.contains(down) && !(down == null)) {//check each state to see if it is in the set already, or it cannot be created
				statesToExplore.push(new State(down)); //if it isnt in set already, and not null, add it to the stack so it can be searched
				RS++; //increase the number of found states by one
				states.add(down); //add the state onto the set of found states
			}
			if(!states.contains(up) && !(up == null)) {
				statesToExplore.push(new State(up));
				RS++;
				states.add(up);
			}
			if(!states.contains(left) && !(left == null)) {
				statesToExplore.push(new State(left));
				RS++;
				states.add(left);
			}
			if(!states.contains(right) && !(right == null)) {
				statesToExplore.push(new State(right));
				RS++;
				states.add(right);
			}
		}		
	}
}

class State{
	//state class so can store infomation and methods about each state
	String tileState;
	public State(String tile){
		this.tileState = tile;
	}
	
	public int blankSpace() {
		//get the index of the blank space
		return this.tileState.indexOf("Z");
	}
	
	public String moveBlank(moveDir dir){
		//this function helps set up for moving the blank space within the state
		//it validates if the blank space can move in the direction proposed
		//if it can move, then it will return the new state,
		//if it cannot move then it will return null
		String tile = this.tileState;
		String newState = null;
		int newIndex;
		int index = this.blankSpace();
		switch(dir) {
		case DOWN:
			if(index > 2) {
				newIndex = index - 3;
				newState = moveTiles(tile, index, newIndex);
			}
			break;
		case LEFT:
			if((index % 3) != 0) {
				newIndex = index - 1;
				newState = moveTiles(tile, index,  newIndex);
			}
			break;
		case RIGHT:
			if(index != 2 && index != 5 && index != 8) {
				newIndex = index + 1;
				newState = moveTiles(tile, index, newIndex);
			}
			break;
		case UP:
			if((index < 6)) {
				newIndex = index + 3;
				newState = moveTiles(tile, index, newIndex);
			}
			break;
		}		
		return newState;
	}
	
	public String moveTiles(String tile, int index, int newIndex) {
		//Splits the state string in to 5 parts:
		//1 - before the first index
		//2 - inbetween the two index's
		//3 - after the last index
		//c1 - first index
		//c2 - second index
		//then puts the indexes back into the order: 1 c2 2 c1 3, this swaps the chars	
		
		String newTile;
		String partOne;
		String partTwo;
		String partThree;
		char charOne = tile.charAt(index);
		char charTwo = tile.charAt(newIndex);
		if(index < newIndex) {
			partOne = tile.substring(0, index);
			partTwo = tile.substring(index+1, newIndex);
			partThree = tile.substring(newIndex+1);
			newTile = partOne + charTwo + partTwo + charOne + partThree;
		} else {
			partOne = tile.substring(0, newIndex);
			partTwo = tile.substring(newIndex+1, index);
			partThree = tile.substring(index+1);
			newTile = partOne + charOne + partTwo + charTwo + partThree;
		}
		return newTile;
		
	}
}
