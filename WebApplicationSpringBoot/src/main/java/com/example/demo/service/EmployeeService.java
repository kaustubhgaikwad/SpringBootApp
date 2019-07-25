package com.example.demo.service;

import java.util.List;

import com.example.demo.model.Employee;

public interface EmployeeService {
	 public List<Employee> getAllEmployees();
	 
	 public Employee findEmployeeById(int id);
	 
	 public void addEmployee(Employee employee);
	 
	 public void updateEmployee(Employee employee);
	 
	 public void deleteEmployee(int id);
	}
