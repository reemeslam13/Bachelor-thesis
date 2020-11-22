package com.example.demo;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Result;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.factory.*;

import java.io.File;

import java.io.File;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Map;
import org.springframework.boot.SpringApplication;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;
@SpringBootApplication
public class Demo2Application implements WebMvcConfigurer {

    private static File DB;
    static GraphDatabaseService movieDB;
    private static File DB2;
    static GraphDatabaseService movieDB2;

    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/home").setViewName("home");
    }

    public static void main(String[] args) {
        SpringApplication.run(Demo2Application.class, args);
    }

}
