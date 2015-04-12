SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `client` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `client` ;

-- -----------------------------------------------------
-- Table `client`.`Cliente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `client`.`Cliente` ;

CREATE  TABLE IF NOT EXISTS `client`.`Cliente` (
  `idClientes` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NOT NULL ,
  `Telefono` VARCHAR(45) NOT NULL ,
  `Mail` VARCHAR(45) NOT NULL ,
  `Sexo` CHAR(1) NOT NULL ,
  `Fecha` DATE NOT NULL ,
  `Usuario` INT NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  PRIMARY KEY (`idClientes`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `client`.`Clientes__tiendas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `client`.`Clientes__tiendas` ;

CREATE  TABLE IF NOT EXISTS `client`.`Clientes__tiendas` (
  `Clientes` INT NOT NULL ,
  `tiendas` INT NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  INDEX `fk_Clientes_has_cliente_tiendas_Clientes_idx` (`Clientes` ASC) ,
  PRIMARY KEY (`Clientes`, `tiendas`) ,
  CONSTRAINT `fk_Clientes_has_cliente_tiendas_Clientes`
    FOREIGN KEY (`Clientes` )
    REFERENCES `client`.`Cliente` (`idClientes` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `client`.`Contrato`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `client`.`Contrato` ;

CREATE  TABLE IF NOT EXISTS `client`.`Contrato` (
  `idContrato` INT NOT NULL AUTO_INCREMENT ,
  `Inicio` DATE NOT NULL ,
  `Fin` DATE NOT NULL ,
  `Fecha` DATE NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `Tienda` INT NOT NULL ,
  `Clientes_idClientes` INT NOT NULL ,
  PRIMARY KEY (`idContrato`) ,
  INDEX `fk_Contrato_Clientes1_idx` (`Clientes_idClientes` ASC) ,
  CONSTRAINT `fk_Contrato_Clientes1`
    FOREIGN KEY (`Clientes_idClientes` )
    REFERENCES `client`.`Cliente` (`idClientes` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `client`.`Privilegios`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `client`.`Privilegios` ;

CREATE  TABLE IF NOT EXISTS `client`.`Privilegios` (
  `idPrivilegios` INT NOT NULL AUTO_INCREMENT ,
  `Nivel` VARCHAR(45) NULL ,
  `Descripcion` TEXT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `Contrato` INT NOT NULL ,
  PRIMARY KEY (`idPrivilegios`) ,
  INDEX `fk_Privilegios_Contrato1_idx` (`Contrato` ASC) ,
  CONSTRAINT `fk_Privilegios_Contrato1`
    FOREIGN KEY (`Contrato` )
    REFERENCES `client`.`Contrato` (`idContrato` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `client`.`Pagos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `client`.`Pagos` ;

CREATE  TABLE IF NOT EXISTS `client`.`Pagos` (
  `idPagos` INT NOT NULL AUTO_INCREMENT ,
  `Forma` VARCHAR(150) NOT NULL ,
  `Monto` DECIMAL(6,2) NOT NULL ,
  `Fecha` DATE NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `Contrato` INT NOT NULL ,
  PRIMARY KEY (`idPagos`) ,
  INDEX `fk_Pagos_Contrato1_idx` (`Contrato` ASC) ,
  CONSTRAINT `fk_Pagos_Contrato1`
    FOREIGN KEY (`Contrato` )
    REFERENCES `client`.`Contrato` (`idContrato` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `client` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
