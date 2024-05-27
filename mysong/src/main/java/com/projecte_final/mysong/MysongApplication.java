package com.projecte_final.mysong;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;

@SpringBootApplication(exclude = {SecurityAutoConfiguration.class})

public class MysongApplication {

	public static void main(String[] args) {
		SpringApplication.run(MysongApplication.class, args);
	}

}
