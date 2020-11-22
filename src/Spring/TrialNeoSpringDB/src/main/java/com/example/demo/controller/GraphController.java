package com.example.demo.controller;

import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Result;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.factory.GraphDatabaseFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.io.File;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

@Controller

public class GraphController {

    private static File DB;
    static GraphDatabaseService movieDB;
    private static File DB2;
    static GraphDatabaseService movieDB2;

    public static void NeoTask1(){

        ArrayList<String[]>data=getDataForGraph(1980,2000);
        for(int i=0;i<data.size();i++){
            System.out.println(data.get(i)[0]+" -> " + data.get(i)[1]);
        }

    }

    //2
    public static ArrayList<String[]>getDataForGraph(int from, int till){
        DB = new File("/Users/reemeslam13/Library/Application Support/Neo4j Desktop/Application/neo4jDatabases/database-680742b5-dcfd-494c-a595-c8d9a073fb11/installation-3.5.3/data/databases/graph.db");
        movieDB = new GraphDatabaseFactory().newEmbeddedDatabase(DB);

        //Small movieDB with int date
        DB2 = new File("/Users/reemeslam13/Library/Application Support/Neo4j Desktop/Application/neo4jDatabases/database-6ed96853-7223-4938-b68f-54f1d3ba5502/installation-3.5.3/data/databases/graph.db");
        movieDB2 = new GraphDatabaseFactory().newEmbeddedDatabase(DB2);
        ArrayList<String[]>data=new ArrayList<String[]>();
        for (int i = from; i <= till; i++) {
            String [] dateNoM=new String[2];
            dateNoM[0]=""+i;
            dateNoM[1]=""+TotalNoMoviesat(i);
            data.add(dateNoM);
        }
        return data;

    }




    static int TotalNoMoviesat(int in) {
        int count = 0;
        try (Transaction ig = movieDB2.beginTx(); Result result = movieDB2.execute("Match(m:Movie) where m.released=" + in +
                " return m")) {

            while (result.hasNext()) {
                result.next();
                count++;
            }
        }

        return count;
    }




    @GetMapping("/displayBarGraph")
    public String barGraph(Model model) {
        Map<String, Integer> surveyMap = new LinkedHashMap<>();
        ArrayList<String[]>data=getDataForGraph(1980,2000);
        for(int i=0;i<data.size();i++){
            surveyMap.put(data.get(i)[0], Integer.parseInt(data.get(i)[1]));

        }
        model.addAttribute("surveyMap", surveyMap);
        return "barGraph";
    }
}
