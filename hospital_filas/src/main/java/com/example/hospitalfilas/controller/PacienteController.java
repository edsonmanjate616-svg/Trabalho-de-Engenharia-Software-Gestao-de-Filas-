package com.example.hospitalfilas.controller;

import com.example.hospitalfilas.model.Paciente;
import com.example.hospitalfilas.repository.PacienteRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/pacientes")
public class PacienteController {

    @Autowired
    private PacienteRepository repository;

    @GetMapping
    public List<Paciente> listar() {
        return repository.findAll();
    }

    @PostMapping
    public Paciente salvar(@RequestBody Paciente paciente) {
        return repository.save(paciente);
    }
}