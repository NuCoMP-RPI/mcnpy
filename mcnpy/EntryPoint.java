import py4j.GatewayServer;

import com.google.inject.Inject;
import com.google.inject.Injector;

import java.io.IOException;

//import org.eclipse.emf.ecore.*;
import org.eclipse.emf.common.util.EList;
import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.util.EcoreUtil;
import org.eclipse.xtext.resource.SaveOptions;
import org.eclipse.xtext.serializer.ISerializer;
import org.eclipse.xtext.xbase.lib.Exceptions;
import org.eclipse.xtext.testing.validation.ValidationTestHelper;
import org.eclipse.emf.ecore.util.EcoreUtil.Copier;
import org.eclipse.emf.ecore.util.EcoreUtil.EqualityHelper;
//import org.eclipse.emf.ecore.resource.impl.ResourceFactoryImpl;

import gov.lanl.mcnp.McnpStandaloneSetup;
import gov.lanl.mcnp.mcnp.*;

@SuppressWarnings("all")
public class EntryPoint {

	@Inject
	public ISerializer serializer;
	
	@Inject
	public ValidationTestHelper validator;
	
	public McnpPackage ePackage = McnpPackage.eINSTANCE;
	
	public Copier copier = new Copier(true);

	/*public EObject copier2(EObject obj)
    {
        Copier copier = new Copier();
        EObject result = copier.copy(obj);
        copier.copyReferences();

        return result;
    }*/
	
	public EqualityHelper equalityHelper = new EqualityHelper();
	
	public ResourceSet resourceSet;

	public McnpFactory factory = McnpFactory.eINSTANCE;

    public String printDeck(Deck DECK)
    {
        //String serializedDeck = this.serializer.serialize(DECK);
        String serializedDeck = this.serializer.serialize(DECK, SaveOptions.newBuilder().format().getOptions());

        return(serializedDeck);
    }

    public String printCELLS(Cells CELLS)
    {
        String serializedDeck = this.serializer.serialize(CELLS);
        
        return(serializedDeck);
    }

    // Reads a deck from a file
	public Deck loadFile(String file)
    {
        try
        {
            Injector injector = new McnpStandaloneSetup().createInjectorAndDoEMFRegistration();
            injector.injectMembers(this);
            ResourceSet resourceSet = injector.<ResourceSet>getInstance(ResourceSet.class);
            //resourceSet.getResourceFactoryRegistry().getExtensionToFactoryMap().put("inp", new ResourceFactoryImpl());
            URI uri = URI.createURI(file);
            //System.out.println("Before Resource Creation\n");
            Resource xtextResource = resourceSet.getResource(uri, true);
            //System.out.println("After Resource Creation\n");
            EcoreUtil.resolveAll(xtextResource);

            Deck DECK = (Deck) (xtextResource.getContents().get(0));
            this.validator.assertNoErrors(DECK);
            
            return(DECK);
        }
        catch (Throwable _e)
        {
            throw Exceptions.sneakyThrow(_e);
        }
    }

    // 
    public Deck deckResource(Deck deck, String filename)
    {
        McnpStandaloneSetup setup = new McnpStandaloneSetup();
        Injector injector = setup.createInjectorAndDoEMFRegistration();
        injector.injectMembers(this);
        ResourceSet resourceSet = injector.<ResourceSet>getInstance(ResourceSet.class);
        URI uri = URI.createURI(filename);
        Resource resource = resourceSet.createResource(uri);

        EList<EObject> _contents = resource.getContents();
        _contents.add(deck);
        Resource xtextResource = resourceSet.getResource(uri, true);
        EcoreUtil.resolveAll(xtextResource);
        return (deck);
    }

    // Creates an empty deck object with empty cell, surface, material, and data ELists.
    public Deck newDeck(String filename)
    {
        McnpStandaloneSetup setup = new McnpStandaloneSetup();
        Injector injector = setup.createInjectorAndDoEMFRegistration();
        injector.injectMembers(this);
        ResourceSet resourceSet = injector.<ResourceSet>getInstance(ResourceSet.class);

        URI uri = URI.createURI(filename);
        Resource resource = resourceSet.createResource(uri);

        Deck DECK = factory.createDeck();
        Surfaces SURFACES = factory.createSurfaces();
        Cells CELLS = factory.createCells();
        Data DATA = factory.createData();

        EList<Surface> surfs = SURFACES.getSurfaces();
        EList<Cell> cells = CELLS.getCells();
        EList<Material> mats = DATA.getMaterials();
        EList<Setting> settings = DATA.getSettings();

        DECK.setCells(CELLS);
        DECK.setSurfaces(SURFACES);
        DECK.setData(DATA);
        EList<EObject> _contents = resource.getContents();
        _contents.add(DECK);
        Resource xtextResource = resourceSet.getResource(uri, true);
        EcoreUtil.resolveAll(xtextResource);

        return(DECK);
    }
	
    public static void main(String[] args) {
        GatewayServer gatewayServer = new GatewayServer(new EntryPoint());
        gatewayServer.start();
        System.out.println("MCNP Gateway Server Started");
    }
    
    public void setup() {
	    McnpStandaloneSetup setup = new McnpStandaloneSetup();
	    Injector injector = setup.createInjectorAndDoEMFRegistration();
	    injector.injectMembers(this);
	    resourceSet = injector.<ResourceSet>getInstance(ResourceSet.class);
    }
}
