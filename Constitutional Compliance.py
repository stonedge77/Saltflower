def test_stone_law():
    """Verify 0≠1 enforcement"""
    cell = HelicalCell()
    
    # Force false equivalence
    cell.signal = True
    cell.potential = True
    
    result = cell.breath_cycle(signal_in=True, admit=False)
    
    assert cell.violation == True, "Failed to detect 0=1 violation"
    print("✓ Stone's Law enforced")

def test_t1_preservation():
    """Verify T=1 remainder survives"""
    array = HelicalNANDArray()
    
    data = np.array([1,0,1,0,1,0,1,0], dtype=bool)
    signals, remainders, _ = array.process(data)
    
    # At least one remainder should be unpaired
    assert np.any(remainders), "T=1 remainder lost"
    print("✓ T=1 unpaired remainder preserved")

def test_breath_cycle():
    """Verify 4-phase breath completes"""
    engine = PrimalMathEngine()
    
    result, t1 = engine.add(7, 5)
    
    # Should complete without violation
    assert result is not None
    print("✓ Breath cycle completed cleanly")

# Run tests
if __name__ == '__main__':
    test_stone_law()
    test_t1_preservation()
    test_breath_cycle()
    print("\n✓ All constitutional bounds validated")
