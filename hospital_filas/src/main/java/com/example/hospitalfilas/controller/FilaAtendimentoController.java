package com.example.hospitalfilas.controller;

import com.example.hospitalfilas.model.FilaAtendimento;
import com.example.hospitalfilas.repository.FilaAtendimentoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/fila")
public class FilaAtendimentoController {

    @Autowired
    private FilaAtendimentoRepository repository;

    @GetMapping
    public List<FilaAtendimento> listar() {
        return repository.findAll();
    }

    @PostMapping
    public FilaAtendimento salvar(@RequestBody FilaAtendimento fila) {
        return repository.save(fila);
    }
}