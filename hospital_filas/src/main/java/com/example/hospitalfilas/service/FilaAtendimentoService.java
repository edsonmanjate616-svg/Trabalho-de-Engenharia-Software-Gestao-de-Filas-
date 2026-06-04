package com.example.hospitalfilas.service;

import com.example.hospitalfilas.model.FilaAtendimento;
import com.example.hospitalfilas.repository.FilaAtendimentoRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class FilaAtendimentoService {

    private final FilaAtendimentoRepository repository;

    public FilaAtendimentoService(FilaAtendimentoRepository repository) {
        this.repository = repository;
    }

    public FilaAtendimento salvar(FilaAtendimento fila) {
        return repository.save(fila);
    }

    public List<FilaAtendimento> listar() {
        return repository.findAll();
    }
}