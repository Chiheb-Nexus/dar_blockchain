pragma solidity ^0.4.0;

contract Balance {
    mapping(address => uint) solde;
    event Transfert(address indexed _from, address indexed _to, uint indexed _amount);
    function transaction(address _to, uint _amount, address _from) public returns (bool) {
        require(_from != _to);
        solde[_from] -= _amount;
        solde[_to] += _amount;
        Transfert(_from, _to, _amount);
        return true;
    }
    
    function getSolde(address _from) public constant returns (uint) {
        return solde[_from];
    }
    
    function addSolde(address _to, uint _amount) public payable returns (bool){
        solde[_to] += _amount;
        return true;
    }
}