SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `tienda` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `tienda` ;

-- -----------------------------------------------------
-- Table `tienda`.`Administrador`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Administrador` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Administrador` (
  `idAdministrador` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NOT NULL ,
  `Login` VARCHAR(45) NOT NULL ,
  `Pass` VARCHAR(45) NOT NULL ,
  `Cliente` VARCHAR(45) NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  PRIMARY KEY (`idAdministrador`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Tienda`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Tienda` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Tienda` (
  `idTienda` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(150) NOT NULL ,
  `RFC` VARCHAR(15) NOT NULL ,
  `Logo` VARCHAR(150) NOT NULL ,
  `Ubicacion` VARCHAR(45) NOT NULL ,
  `Direccion` VARCHAR(45) NOT NULL ,
  `Mail` VARCHAR(45) NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `Telefono` VARCHAR(45) NOT NULL ,
  `Descripcion` TEXT NULL ,
  `Administrador` INT NOT NULL ,
  PRIMARY KEY (`idTienda`) ,
  INDEX `fk_Tienda_Administrador_idx` (`Administrador` ASC) ,
  CONSTRAINT `fk_Tienda_Administrador`
    FOREIGN KEY (`Administrador` )
    REFERENCES `tienda`.`Administrador` (`idAdministrador` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Stock`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Stock` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Stock` (
  `idStock` INT NOT NULL AUTO_INCREMENT ,
  `Fecha` DATE NOT NULL ,
  `Descripcion` TEXT NOT NULL ,
  `Tienda` INT NOT NULL ,
  PRIMARY KEY (`idStock`) ,
  CONSTRAINT `fk_Stock_Tienda1`
    FOREIGN KEY (`Tienda` )
    REFERENCES `tienda`.`Tienda` (`idTienda` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`TipoCliente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`TipoCliente` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`TipoCliente` (
  `idTipoCliente` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NULL ,
  `Descripcion` TEXT NULL ,
  `Prioridad` CHAR(1) NULL ,
  `Stock_idStock` INT NOT NULL ,
  PRIMARY KEY (`idTipoCliente`) ,
  INDEX `fk_TipoCliente_Stock1_idx` (`Stock_idStock` ASC) ,
  CONSTRAINT `fk_TipoCliente_Stock1`
    FOREIGN KEY (`Stock_idStock` )
    REFERENCES `tienda`.`Stock` (`idStock` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Clientes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Clientes` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Clientes` (
  `idClientes` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(150) NOT NULL ,
  `Domicilio` VARCHAR(200) NOT NULL ,
  `CP` VARCHAR(20) NOT NULL ,
  `Estado` VARCHAR(20) NOT NULL ,
  `Mail` VARCHAR(100) NOT NULL ,
  `tel` VARCHAR(50) NOT NULL ,
  `pass` VARCHAR(45) NOT NULL ,
  `TipoCliente` INT NOT NULL ,
  `Tienda` INT NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  PRIMARY KEY (`idClientes`) ,
  INDEX `fk_Clientes_TipoCliente1_idx` (`TipoCliente` ASC) ,
  INDEX `fk_Clientes_Tienda1_idx` (`Tienda` ASC) ,
  CONSTRAINT `fk_Clientes_TipoCliente1`
    FOREIGN KEY (`TipoCliente` )
    REFERENCES `tienda`.`TipoCliente` (`idTipoCliente` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Clientes_Tienda1`
    FOREIGN KEY (`Tienda` )
    REFERENCES `tienda`.`Tienda` (`idTienda` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Unidades`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Unidades` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Unidades` (
  `Nombre` VARCHAR(50) NOT NULL ,
  `prefijo` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`Nombre`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Categorias`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Categorias` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Categorias` (
  `idCategorias` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(100) NOT NULL ,
  `Descripcion` VARCHAR(150) NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `Stock` INT NOT NULL ,
  INDEX `fk_Categorias_Stock1_idx` (`Stock` ASC) ,
  PRIMARY KEY (`idCategorias`) ,
  CONSTRAINT `fk_Categorias_Stock1`
    FOREIGN KEY (`Stock` )
    REFERENCES `tienda`.`Stock` (`idStock` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Productos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Productos` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Productos` (
  `idProductos` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(250) NOT NULL ,
  `Descripcion` TEXT NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `Precio` DECIMAL(10,2) NOT NULL ,
  `Unidad` VARCHAR(50) NOT NULL ,
  `Categorias` INT NOT NULL ,
  PRIMARY KEY (`idProductos`) ,
  INDEX `fk_Productos_Unidades1_idx` (`Unidad` ASC) ,
  INDEX `fk_Productos_Categorias1_idx` (`Categorias` ASC) ,
  CONSTRAINT `fk_Productos_Unidades1`
    FOREIGN KEY (`Unidad` )
    REFERENCES `tienda`.`Unidades` (`Nombre` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Productos_Categorias1`
    FOREIGN KEY (`Categorias` )
    REFERENCES `tienda`.`Categorias` (`idCategorias` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`FormaPago`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`FormaPago` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`FormaPago` (
  `Nombre` VARCHAR(45) NOT NULL ,
  `Descripcion` TEXT NULL ,
  `Logo` VARCHAR(45) NULL ,
  PRIMARY KEY (`Nombre`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Zonas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Zonas` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Zonas` (
  `idZonas` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NOT NULL ,
  `Descripcion` VARCHAR(45) NOT NULL ,
  `Estados` TEXT NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `Tienda` INT NOT NULL ,
  PRIMARY KEY (`idZonas`) ,
  INDEX `fk_Zonas_Tienda1_idx` (`Tienda` ASC) ,
  CONSTRAINT `fk_Zonas_Tienda1`
    FOREIGN KEY (`Tienda` )
    REFERENCES `tienda`.`Tienda` (`idTienda` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`FormaEnvio`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`FormaEnvio` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`FormaEnvio` (
  `idFormaEnvio` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NOT NULL ,
  `Datos` TEXT NOT NULL ,
  `Logo` VARCHAR(150) NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  PRIMARY KEY (`idFormaEnvio`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Pedidos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Pedidos` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Pedidos` (
  `idPedidos` INT NOT NULL AUTO_INCREMENT ,
  `Fecha` DATE NOT NULL ,
  `Clientes` INT NOT NULL ,
  `Stock` INT NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `Comentarios` TEXT NOT NULL ,
  `status` VARCHAR(45) NOT NULL ,
  `DireccionEnvio` TEXT NOT NULL ,
  `Estado` TINYINT(1) NOT NULL ,
  `Importe` DECIMAL(10,2) NOT NULL ,
  `ImporteEnvio` DECIMAL(10,2) NOT NULL ,
  `CPE` VARCHAR(45) NOT NULL ,
  `Zonas` INT NOT NULL ,
  `FormaEnvio` INT NOT NULL ,
  PRIMARY KEY (`idPedidos`) ,
  INDEX `fk_Pedidos_Zonas1_idx` (`Zonas` ASC) ,
  INDEX `fk_Pedidos_FormaEnvio1_idx` (`FormaEnvio` ASC) ,
  CONSTRAINT `fk_Pedidos_Clientes1`
    FOREIGN KEY (`Clientes` )
    REFERENCES `tienda`.`Clientes` (`idClientes` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Pedidos_Stock1`
    FOREIGN KEY (`Stock` )
    REFERENCES `tienda`.`Stock` (`idStock` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Pedidos_Zonas1`
    FOREIGN KEY (`Zonas` )
    REFERENCES `tienda`.`Zonas` (`idZonas` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Pedidos_FormaEnvio1`
    FOREIGN KEY (`FormaEnvio` )
    REFERENCES `tienda`.`FormaEnvio` (`idFormaEnvio` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Promociones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Promociones` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Promociones` (
  `idPromociones` INT NOT NULL ,
  `Codigo` VARCHAR(45) NULL ,
  `FechaInicio` DATE NULL ,
  `FechaFinal` DATE NULL ,
  `Descripcion` TEXT NULL ,
  `Imagen` VARCHAR(250) NULL ,
  `Stock` INT NOT NULL ,
  PRIMARY KEY (`idPromociones`) ,
  INDEX `fk_Promociones_Stock1_idx` (`Stock` ASC) ,
  CONSTRAINT `fk_Promociones_Stock1`
    FOREIGN KEY (`Stock` )
    REFERENCES `tienda`.`Stock` (`idStock` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Productos_Promociones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Productos_Promociones` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Productos_Promociones` (
  `Productos` INT NOT NULL ,
  `Promociones` INT NOT NULL ,
  `Descuento` DECIMAL(4,2) NULL ,
  `Cantidad` DECIMAL(4,2) NULL ,
  PRIMARY KEY (`Productos`, `Promociones`) ,
  INDEX `fk_Productos_has_Promociones_Promociones1_idx` (`Promociones` ASC) ,
  INDEX `fk_Productos_has_Promociones_Productos1_idx` (`Productos` ASC) ,
  CONSTRAINT `fk_Productos_has_Promociones_Productos1`
    FOREIGN KEY (`Productos` )
    REFERENCES `tienda`.`Productos` (`idProductos` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Productos_has_Promociones_Promociones1`
    FOREIGN KEY (`Promociones` )
    REFERENCES `tienda`.`Promociones` (`idPromociones` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Promociones_TipoCliente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Promociones_TipoCliente` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Promociones_TipoCliente` (
  `Promociones` INT NOT NULL ,
  `TipoCliente` INT NOT NULL ,
  PRIMARY KEY (`Promociones`, `TipoCliente`) ,
  INDEX `fk_Promociones_has_TipoCliente_TipoCliente1_idx` (`TipoCliente` ASC) ,
  INDEX `fk_Promociones_has_TipoCliente_Promociones1_idx` (`Promociones` ASC) ,
  CONSTRAINT `fk_Promociones_has_TipoCliente_Promociones1`
    FOREIGN KEY (`Promociones` )
    REFERENCES `tienda`.`Promociones` (`idPromociones` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Promociones_has_TipoCliente_TipoCliente1`
    FOREIGN KEY (`TipoCliente` )
    REFERENCES `tienda`.`TipoCliente` (`idTipoCliente` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Tienda_FormaEnvio`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Tienda_FormaEnvio` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Tienda_FormaEnvio` (
  `Tienda` INT NOT NULL ,
  `FormaEnvio` INT NOT NULL ,
  `Activo` TINYINT(1) NOT NULL DEFAULT 1 ,
  PRIMARY KEY (`Tienda`, `FormaEnvio`) ,
  INDEX `fk_Tienda_has_FormaEnvio_FormaEnvio1_idx` (`FormaEnvio` ASC) ,
  INDEX `fk_Tienda_has_FormaEnvio_Tienda1_idx` (`Tienda` ASC) ,
  CONSTRAINT `fk_Tienda_has_FormaEnvio_Tienda1`
    FOREIGN KEY (`Tienda` )
    REFERENCES `tienda`.`Tienda` (`idTienda` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Tienda_has_FormaEnvio_FormaEnvio1`
    FOREIGN KEY (`FormaEnvio` )
    REFERENCES `tienda`.`FormaEnvio` (`idFormaEnvio` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Tienda_FormaPago`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Tienda_FormaPago` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Tienda_FormaPago` (
  `Tienda` INT NOT NULL ,
  `FormaPago` VARCHAR(45) NOT NULL ,
  `LlavePrivada` VARCHAR(100) NOT NULL ,
  `LlavePublica` VARCHAR(100) NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  PRIMARY KEY (`Tienda`, `FormaPago`) ,
  INDEX `fk_Tienda_has_FormaPago_FormaPago1_idx` (`FormaPago` ASC) ,
  INDEX `fk_Tienda_has_FormaPago_Tienda1_idx` (`Tienda` ASC) ,
  CONSTRAINT `fk_Tienda_has_FormaPago_Tienda1`
    FOREIGN KEY (`Tienda` )
    REFERENCES `tienda`.`Tienda` (`idTienda` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Tienda_has_FormaPago_FormaPago1`
    FOREIGN KEY (`FormaPago` )
    REFERENCES `tienda`.`FormaPago` (`Nombre` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Paquetes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Paquetes` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Paquetes` (
  `idPaquetes` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NOT NULL ,
  `Maximo` VARCHAR(45) NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `Tienda` INT NOT NULL ,
  PRIMARY KEY (`idPaquetes`) ,
  INDEX `fk_Paquetes_Tienda1_idx` (`Tienda` ASC) ,
  CONSTRAINT `fk_Paquetes_Tienda1`
    FOREIGN KEY (`Tienda` )
    REFERENCES `tienda`.`Tienda` (`idTienda` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Paquetes_FormaEnvio`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Paquetes_FormaEnvio` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Paquetes_FormaEnvio` (
  `Paquetes` INT NOT NULL ,
  `FormaEnvio` INT NOT NULL ,
  `Zonas` INT NOT NULL ,
  `Activo` TINYINT(1) NULL ,
  `Importe` DECIMAL(6,2) NULL ,
  PRIMARY KEY (`Paquetes`, `FormaEnvio`, `Zonas`) ,
  INDEX `fk_Paquetes_has_FormaEnvio_FormaEnvio1_idx` (`FormaEnvio` ASC) ,
  INDEX `fk_Paquetes_has_FormaEnvio_Paquetes1_idx` (`Paquetes` ASC) ,
  INDEX `fk_Paquetes_FormaEnvio_Zonas1_idx` (`Zonas` ASC) ,
  CONSTRAINT `fk_Paquetes_has_FormaEnvio_Paquetes1`
    FOREIGN KEY (`Paquetes` )
    REFERENCES `tienda`.`Paquetes` (`idPaquetes` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Paquetes_has_FormaEnvio_FormaEnvio1`
    FOREIGN KEY (`FormaEnvio` )
    REFERENCES `tienda`.`FormaEnvio` (`idFormaEnvio` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Paquetes_FormaEnvio_Zonas1`
    FOREIGN KEY (`Zonas` )
    REFERENCES `tienda`.`Zonas` (`idZonas` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Paquetes_Categorias`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Paquetes_Categorias` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Paquetes_Categorias` (
  `Paquetes` INT NOT NULL ,
  `Categorias` INT NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  PRIMARY KEY (`Paquetes`, `Categorias`) ,
  INDEX `fk_Paquetes_has_Categorias_Categorias1_idx` (`Categorias` ASC) ,
  INDEX `fk_Paquetes_has_Categorias_Paquetes1_idx` (`Paquetes` ASC) ,
  CONSTRAINT `fk_Paquetes_has_Categorias_Paquetes1`
    FOREIGN KEY (`Paquetes` )
    REFERENCES `tienda`.`Paquetes` (`idPaquetes` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Paquetes_has_Categorias_Categorias1`
    FOREIGN KEY (`Categorias` )
    REFERENCES `tienda`.`Categorias` (`idCategorias` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Imagenes_producto`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Imagenes_producto` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Imagenes_producto` (
  `idImagenes_producto` INT NOT NULL AUTO_INCREMENT ,
  `Archivo` VARCHAR(45) NOT NULL ,
  `prioridad` VARCHAR(45) NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `Productos` INT NOT NULL ,
  PRIMARY KEY (`idImagenes_producto`) ,
  INDEX `fk_Imagenes_producto_Productos1_idx` (`Productos` ASC) ,
  CONSTRAINT `fk_Imagenes_producto_Productos1`
    FOREIGN KEY (`Productos` )
    REFERENCES `tienda`.`Productos` (`idProductos` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Extras`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Extras` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Extras` (
  `idtable1` INT NOT NULL AUTO_INCREMENT ,
  `Concepto` VARCHAR(45) NULL ,
  `Valor` DECIMAL(6,2) NULL ,
  `tipo` VARCHAR(45) NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `Pedidos` INT NOT NULL ,
  PRIMARY KEY (`idtable1`) ,
  INDEX `fk_Extras_Pedidos1_idx` (`Pedidos` ASC) ,
  CONSTRAINT `fk_Extras_Pedidos1`
    FOREIGN KEY (`Pedidos` )
    REFERENCES `tienda`.`Pedidos` (`idPedidos` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Modelos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Modelos` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Modelos` (
  `idModelos` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NOT NULL ,
  `Precio` DECIMAL(6,2) NOT NULL ,
  `Descripcion` TEXT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `Existencias` DECIMAL(5,2) NOT NULL ,
  `Productos` INT NOT NULL ,
  PRIMARY KEY (`idModelos`) ,
  INDEX `fk_Modelos_Productos1_idx` (`Productos` ASC) ,
  CONSTRAINT `fk_Modelos_Productos1`
    FOREIGN KEY (`Productos` )
    REFERENCES `tienda`.`Productos` (`idProductos` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Pedidos_Productos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Pedidos_Productos` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Pedidos_Productos` (
  `Pedidos` INT NOT NULL ,
  `Productos` INT NOT NULL ,
  `Modelos` INT NOT NULL ,
  `Cantidad` DECIMAL(10,2) NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  PRIMARY KEY (`Pedidos`, `Productos`, `Modelos`) ,
  INDEX `fk_Pedidos_has_Productos_Productos1_idx` (`Productos` ASC) ,
  INDEX `fk_Pedidos_has_Productos_Pedidos1_idx` (`Pedidos` ASC) ,
  INDEX `fk_Pedidos_Productos_Modelos1_idx` (`Modelos` ASC) ,
  CONSTRAINT `fk_Pedidos_has_Productos_Pedidos1`
    FOREIGN KEY (`Pedidos` )
    REFERENCES `tienda`.`Pedidos` (`idPedidos` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Pedidos_has_Productos_Productos1`
    FOREIGN KEY (`Productos` )
    REFERENCES `tienda`.`Productos` (`idProductos` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Pedidos_Productos_Modelos1`
    FOREIGN KEY (`Modelos` )
    REFERENCES `tienda`.`Modelos` (`idModelos` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Galeria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Galeria` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Galeria` (
  `idGaleria` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NOT NULL ,
  `Archivo` VARCHAR(45) NOT NULL ,
  `Tipo` CHAR(1) NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `Productos` INT NOT NULL ,
  PRIMARY KEY (`idGaleria`) ,
  INDEX `fk_Galeria_Productos1_idx` (`Productos` ASC) ,
  CONSTRAINT `fk_Galeria_Productos1`
    FOREIGN KEY (`Productos` )
    REFERENCES `tienda`.`Productos` (`idProductos` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Anuncios`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Anuncios` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Anuncios` (
  `idAnuncios` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NOT NULL ,
  `Fecha` TIMESTAMP NOT NULL ,
  `Imagen` VARCHAR(145) NOT NULL ,
  `Descripcion` TEXT NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `Tipo` CHAR NOT NULL ,
  `Tienda` INT NOT NULL ,
  PRIMARY KEY (`idAnuncios`) ,
  INDEX `fk_Anuncios_Tienda1_idx` (`Tienda` ASC) ,
  CONSTRAINT `fk_Anuncios_Tienda1`
    FOREIGN KEY (`Tienda` )
    REFERENCES `tienda`.`Tienda` (`idTienda` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Cargos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Cargos` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Cargos` (
  `idCargo` VARCHAR(150) NOT NULL ,
  `Fecha` DATE NOT NULL ,
  `status` CHAR(1) NOT NULL ,
  `Importe` INT NOT NULL ,
  `Activo` TINYINT(1) NOT NULL DEFAULT 1 ,
  `FormaPago` VARCHAR(45) NOT NULL ,
  `Pedidos` INT NOT NULL ,
  INDEX `fk_Cargos_FormaPago1_idx` (`FormaPago` ASC) ,
  INDEX `fk_Cargos_Pedidos1_idx` (`Pedidos` ASC) ,
  PRIMARY KEY (`idCargo`) ,
  CONSTRAINT `fk_Cargos_FormaPago1`
    FOREIGN KEY (`FormaPago` )
    REFERENCES `tienda`.`FormaPago` (`Nombre` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Cargos_Pedidos1`
    FOREIGN KEY (`Pedidos` )
    REFERENCES `tienda`.`Pedidos` (`idPedidos` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tienda`.`Referencia`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tienda`.`Referencia` ;

CREATE  TABLE IF NOT EXISTS `tienda`.`Referencia` (
  `idReferencia` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NULL ,
  `Valor` VARCHAR(250) NULL ,
  `Cargos` VARCHAR(150) NOT NULL ,
  PRIMARY KEY (`idReferencia`) ,
  INDEX `fk_Referencia_Cargos1_idx` (`Cargos` ASC) ,
  CONSTRAINT `fk_Referencia_Cargos1`
    FOREIGN KEY (`Cargos` )
    REFERENCES `tienda`.`Cargos` (`idCargo` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `tienda` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
