import java.util.HashSet;
import java.util.Scanner;

public class KC {
	public static void main(String args[]) {
		Scanner scan = new Scanner(System.in);
		String input = "";
		String trace = "";
		HashSet <String> F = new HashSet<String>(); 
		boolean flag = true;
		input = scan.nextLine();
		int i = Integer.parseInt(input);
		for(int x=0;x<i;x++) {
			trace +="1";
			String temp="";
			for(int y=0;y<x;y++) {
				temp+="0";
			}
			temp+="1";
			F.add(temp);
		}
		String output = "";
		for(int x=0;x<i;x++) {
			output+="0";
		}
		System.out.println("output:"+output);
		System.out.println("trace:"+trace);
		System.out.println("F:"+F);
		while(flag) {
			input = scan.nextLine();
			if(input.isEmpty()) {
				System.out.println("input is illegalhere");
				continue;
			}
			i = Integer.parseInt(input);
			int num = trace.length()-i;
			if(num<0) {
				num = -num;
				for(int x=1;x<=num;x++) {
					trace+="0";
				}
			}
			int position = i-1;
			while(position>=0 && trace.charAt(position)!='1' ) {
				position--;
			}
			if(position==-1) {
				System.out.println("the input is illegal");
				continue;
			}else {
				// update the set F
				F = updateF(F,position,i);
				//update the trace.
				String formerPart = trace.substring(0, position);
				String rearPart = "";
				formerPart+="0";
				for(int x = position+1;x < i;x++) {
					formerPart+="1";
				}
				if(trace.length()==i) {
					rearPart = "";
				}else {
					rearPart = trace.substring(i);
				}
				trace = formerPart+rearPart;
			}
			
			System.out.println("trace:"+trace);
			System.out.println("F:"+F);
		}
	}
	
	public static HashSet<String>updateF(HashSet<String> F,int positon,int requiredLen){
		for(String s : F){
			if(s.length() > positon)
			if(s.charAt(positon)=='1') {
				String ss = s;
				F.remove(s);
				if(ss.length()<requiredLen) {
					int num1 = requiredLen-ss.length();
					for(int x = 0;x<num1;x++) {
						ss+="0";
					}
					System.out.println("output:"+ss);
					for(int x=0;x<=num1-1;x++) {
						String tt = "";
						String sss =s;
						for(int y=1;y<=x;y++) {
							tt+="0";
						}
						sss += tt ;
						sss += "1";
						F.add(sss);
					}
				}else {
					System.out.println("output:"+ss);
				}
				break;
			}
		}
		return F;	
	}
}
 