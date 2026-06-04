package com.example.hospitalfilas.repository;

import com.example.hospitalfilas.model.Paciente;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PacienteRepository extends JpaRepository<Paciente, Long> {

}