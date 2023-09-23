import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

class Problem054 {
    
    public static Hashtable<String, Integer> numbers = new Hashtable<String, Integer>();
    public static Hashtable<String, Integer> winTypes = new Hashtable<String, Integer>();
    public static int p1Wins = 0;
    public static int p2Wins = 0;

    
    public static void populateNumbers(){
        numbers.put("2", 2);
        numbers.put("3", 3);
        numbers.put("4", 4);
        numbers.put("5", 5);
        numbers.put("6", 6);
        numbers.put("7", 7);
        numbers.put("8", 8);
        numbers.put("9", 9);
        numbers.put("T", 10);
        numbers.put("J", 11);
        numbers.put("Q", 12);
        numbers.put("K", 13);
        numbers.put("A", 14);
    }
    
    public static void populateWinTypes(){
        // Win Type, Score
        winTypes.put("High Card", 1);
        winTypes.put("One Pair", 2);
        winTypes.put("Two Pairs", 3);
        winTypes.put("Three of a Kind", 4);
        winTypes.put("Straight", 5);
        winTypes.put("Flush", 6);
        winTypes.put("Full House", 7);
        winTypes.put("Four of a Kind", 8);
        winTypes.put("Straight Flush", 9);
        winTypes.put("Royal Flush", 10);
    }
    
    public static boolean areConsecutive(List<String> al){
        List<Integer> iaL = new ArrayList<Integer>();
        for(String s : al){
            iaL.add(numbers.get(s));
        }
        
        Collections.sort(iaL);
        
        boolean flag = true;
        for(int x = 1; x<iaL.size(); x++){
            if(iaL.get(x) != iaL.get(x-1) + 1){
                flag = false;
                break;
            }
        }
        return flag;
    }
    
    public static String calculateWinType(List<String> cards){
        
        List<String> v = new ArrayList<String>();
        Set<String> s = new HashSet<String>();
        
        List<String> topFive = new ArrayList<String>();
        topFive.add("T");
        topFive.add("J");
        topFive.add("Q");
        topFive.add("K");
        topFive.add("A");
        
        for(String c : cards){
            v.add(c.substring(0, 1));
            s.add(c.substring(1));
        }
        
        int card1 = Collections.frequency(v, v.get(0));
        int card2 = Collections.frequency(v, v.get(1));
        int card3 = Collections.frequency(v, v.get(2));
        int card4 = Collections.frequency(v, v.get(3));
        int card5 = Collections.frequency(v, v.get(4));
        
        //System.out.println(v);
        //System.out.println(s);
        
        if( s.size() == 1 && v.containsAll(topFive) ){
            return "Royal Flush";
        } else if( s.size() == 1 && areConsecutive(v) ){
            return "Straight Flush";
        } else if( card1 == 4 || card2 == 4 ){
            return "Four of a Kind";
        } else if( (card1 == 3 || card2 == 3 || card3 == 3) && (card1 == 2 || card2 == 2 || card3 == 2 || card4 == 2) ){
            return "Full House";
        } else if( s.size() == 1 ){
            return "Flush";
        } else if ( areConsecutive(v) ){
            return "Straight";
        } else if(card1 == 3 || card2 == 3 || card3 == 3){
            return "Three of a Kind";
        } else if(card1*card2*card3*card4*card5 == 16){
            return "Two Pairs";
        } else if(card1 == 2 || card2 == 2 || card3 == 2 || card4 == 2){
            return "One Pair";
        } else {
            return "High Card";
        }
    }

    public static void scoring(String p1Res, String p2Res, List<String> cardsP1, List<String> cardsP2){
        int p1Score = winTypes.get(p1Res);
        int p2Score = winTypes.get(p2Res);

        //System.out.println("P1: " + p1Res + " " + cardsP1);
        //System.out.println("P2: " + p2Res + " " + cardsP2);
        
        if(p1Score == p2Score){
            List<Integer> valsP1 = new ArrayList<Integer>();
            List<Integer> valsP2 = new ArrayList<Integer>();
            for(String c : cardsP1){
                valsP1.add(numbers.get(c.substring(0, 1)));
            }

            for(String c : cardsP2){
                valsP2.add(numbers.get(c.substring(0, 1)));
            }
            
            int p1High = 0;
            int p2High = 0;
            
            if(p1Score == 1){
                p1High = Collections.max(valsP1);
                p2High = Collections.max(valsP2);
                
            } else {
                for(int i = 0; i<valsP1.size(); i++){
                    if(Collections.frequency(valsP1, valsP1.get(i)) == 2){
                        p1High = valsP1.get(i);
                        break;
                    }
                }
                
                for(int i = 0; i<valsP2.size(); i++){
                    if(Collections.frequency(valsP2, valsP2.get(i)) == 2){
                        p2High = valsP2.get(i);
                        break;
                    }
                }
            }
            
            if(p1High > p2High){
                p1Wins++;
                //System.out.println("P1 is the Winner!");
            } else {
                p2Wins++;
                //System.out.println("P2 is the Winner!");
            }

        } else {
            if(p1Score>p2Score){
                p1Wins++;
                //System.out.println("P1 is the Winner!");
            } else {
                p2Wins++;
                //System.out.println("P2 is the Winner!");
            }
        }
    }
    
    public static void main(String[] args) throws IOException {

        populateNumbers();
        populateWinTypes();

        for(int line = 0; line<data.length; line++) {
            String cards[] = data[line].split(" ");
            List<String> cardsP1 = Arrays.asList(cards).subList(0, 5);
            List<String> cardsP2 = Arrays.asList(cards).subList(5, 10);
            
            String p1Result = calculateWinType(cardsP1);
            String p2Result = calculateWinType(cardsP2);
            scoring(p1Result, p2Result, cardsP1, cardsP2);
        }


        System.out.println("P1 wins: " + p1Wins);
        
        
    }
    
    public static String[] data = new String[]{
        "8C TS KC 9H 4S 7D 2S 5D 3S AC",
        "...",
        "...",
        "...",
        "AS KD 3D JD 8H 7C 8C 5C QD 6C"
    };

}
