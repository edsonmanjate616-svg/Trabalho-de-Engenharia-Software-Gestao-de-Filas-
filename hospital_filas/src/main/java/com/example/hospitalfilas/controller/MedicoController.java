package com.example.hospitalfilas.controller;

import com.example.hospitalfilas.model.Medico;
import com.example.hospitalfilas.repository.MedicoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/medicos")
public class MedicoController {

    @Autowired
    private MedicoRepository repository;

    @GetMapping
    public List<Medico> listar() {
        return repository.findAll();
    }

    @PostMapping
    public Medico salvar(@RequestBody Medico medico) {
        return repository.save(medico);
    }
}