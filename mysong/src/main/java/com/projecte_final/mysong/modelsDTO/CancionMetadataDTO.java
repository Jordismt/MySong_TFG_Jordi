package com.projecte_final.mysong.modelsDTO;

import lombok.Data;

@Data
public class CancionMetadataDTO {

    private Long id;
    private String nombre;
    private String artista;
    private String album;
    private String nombreArchivo;
    // Otros metadatos necesarios

    // Getters y setters
}

